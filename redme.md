check kafka topics: kafka-topics --list --bootstrap-server broker:29092

consume messages from topic: kafka-console-consumer --topic voter_topic --bootstrap-server broker:29092




consume messages from topic: kafka-console-consumer --topic aggregated_votes_per_candidate --bootstrap-server broker:29092





kafka-topics --describe --topic aggregated_votes_per_candidate --bootstrap-server localhost:9092
