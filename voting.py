import json
from get_db_connection import connect_to_db
from confluent_kafka import Consumer, KafkaException, KafkaError, SerializingProducer
import random
import time
from datetime import datetime
from main import delivery_report



conf = {
    'bootstrap.servers': 'localhost:9092',
}

consumer = Consumer(conf | {
    'group.id': 'voting-group',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False
})

producer = SerializingProducer(conf)



def main():
    try:
        cur.close()
        conn.close()
    except:
        pass
    conn, cur = connect_to_db()

    # candidates
    candidates_res = """
                        SELECT row_to_json(t)
                        FROM (
                            SELECT * FROM candidates
                        ) t;
                    """
    cur.execute(candidates_res)

    candidates = [candidate[0] for candidate in cur.fetchall()]

    if len(candidates) == 0:
        raise ValueError("No candidates found in the database")
    else:
        d = 'ys'

    consumer.subscribe(['voters_topics'])
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            elif msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break
            else:
                voter = json.loads(msg.value().decode('utf-8'))
                chosen_candidate = random.choice(candidates)
                vote = voter | chosen_candidate | {
                    'voting_time': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                    'vote': 1
                }

                try:
                    print("User {} is voting for candidate: {}".format(vote['voter_id'], vote['candidate_id']))
                    cur.execute("""
                            INSERT INTO votes (voter_id, candidate_id, voting_time)
                            VALUES (%s, %s, %s)
                        """, (vote['voter_id'], vote['candidate_id'], vote['voting_time']))

                    conn.commit()
                    producer.produce(
                        'votes_topic',
                        key=vote['voter_id'],
                        value=json.dumps(vote),
                        on_delivery=delivery_report
                    )
                    producer.poll(0)
                except Exception as e:
                    print("Error: {}".format(e))
                    conn.rollback()
                    continue
            time.sleep(0.2)

    except KafkaException as e:
        print(e)
    
    try:
        cur.close()
        conn.close()
    except:
        pass


if __name__ == "__main__":
    main()