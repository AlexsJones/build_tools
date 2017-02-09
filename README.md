# ce-devops-stats
Stats service for ce-devices teams 

To Launch with docker 

```
docker run -p 0.0.0.0:2001:2001 -it <container-id> /bin/bash
```
```
gunicorn app:app --bind 0.0.0.0:2001 --reload
```

