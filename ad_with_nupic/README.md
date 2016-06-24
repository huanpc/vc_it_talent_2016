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

1. Run swarm.py to create best model params for input file(that file converted from .json): `python swarm.py`
2. Run run.py: `python run.py`

# Documentation

1. [Nupic Wiki](https://github.com/numenta/nupic/wiki)
