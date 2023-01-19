# social_media_app_API

## Setting up the API

1) Make sure that you have python3 and docker desktop installed in your system
2) Create a venvironment and activate venv
3) execute "pip install -r requirements.txt"

Next to setup the dockerized postgres sql
1) Navigate to this docker hub repository https://hub.docker.com/repository/docker/sanjeevkm/social_media_postgres/tags?page=1&ordering=last_updated
2) Pull this image using "docker pull sanjeevkm/social_media_postgres:latest"
3) And start the container on this image
4) Now the postgres service will be availabe at "localhost:5432"

Next navigating to flask, you can start the endpoint using "flask run" command

## List of endpoints

http://127.0.0.1:5000/messages - GET : Returns all messages (newest message first)
http://127.0.0.1:5000/messages - POST : Create a new message
http://127.0.0.1:5000/likes/<message_id> - POST : Add like to a message

# APPENDIX

## SQL Tables and Trigger function

### Message Table
```
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    message TEXT NOT NULL,
    likes INTEGER DEFAULT 0,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Likes Table
```
CREATE TABLE likes (
     id SERIAL PRIMARY KEY,
     message_id INTEGER REFERENCES messages(id),
     timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Trigger Function to update likes in messages table after like is added into likes table
```
CREATE OR REPLACE FUNCTION update_likes() RETURNS TRIGGER AS $$
BEGIN
     UPDATE messages SET likes = (SELECT COUNT(*) FROM likes WHERE message_id = NEW.message_id) WHERE id = NEW.message_id;
     RETURN NULL;
END;
$$ LANGUAGE plpgsql;
```

### Trigger
```
CREATE TRIGGER update_likes_count
AFTER INSERT OR DELETE ON likes
FOR EACH ROW
EXECUTE FUNCTION update_likes();
```
