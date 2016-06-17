# Anomaly Detection with Nupic - Kien Nguyen (Base on Nupic Anomaly Detection example)

## Prerequisites

1. Install Mysql.
2. Run the following commands: `mysql -u root -p`

```
> use mysql;
> update user set password=null where User='root' and Host='localhost';
> flush privileges;
```

3. Test DB connection: `python $NUPIC/examples/swarm/test_db.py`

# Run

1. Run swarm.py(still get error): `python swarm.py`
2. Run run.py: `python run.py`
