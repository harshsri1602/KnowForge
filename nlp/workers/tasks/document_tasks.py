from nlp.workers.celery_app import celery_app
from nlp.pipeline import run_nlp_pipeline
import psycopg2

@celery_app.task
def poll_documents():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE documents
        SET status = 'processing'
        WHERE id IN (
            SELECT id FROM documents
            WHERE status = 'pending'
            ORDER BY created_at ASC
            LIMIT 5
            FOR UPDATE SKIP LOCKED
        )
        RETURNING id
    """)

    rows = cur.fetchall()
    conn.commit()

    doc_ids = [row[0] for row in rows]

    cur.close()
    conn.close()

    for doc_id in doc_ids:
        process_document.delay(doc_id)

    return f"Dispatched {len(doc_ids)} documents"

@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3})
def process_document(self, doc_id: int):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT content, metadata
            FROM documents
            WHERE id = %s
        """, (doc_id,))

        row = cur.fetchone()

        if not row:
            return f"Document {doc_id} not found"

        content, metadata = row

        record = {
            "content": content,
            "metadata": metadata
        }

        result = run_nlp_pipeline(record["content"])

        cur.execute("""
            UPDATE documents
            SET status = 'nlp_finished'
            WHERE id = %s
        """, (doc_id,))

        conn.commit()
        print(result)

        return f"Processed document {doc_id}"

    except Exception as e:
        conn.rollback()

        cur.execute("""
            UPDATE documents
            SET status = 'failed'
            WHERE id = %s
        """, (doc_id,))

        conn.commit()

        raise self.retry(exc=e)

    finally:
        cur.close()
        conn.close()
        
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="harsh"
    )