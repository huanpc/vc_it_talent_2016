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

1. Run swarm.py to create best model params for input file(that file converted from .json) if you don't have this yet. It will take a long time to execute: `python swarm.py`
2. Run run.py for execute anomaly detection. If you want to visualize result with mathplot use flag --plot: `python run.py` or `python run.py --plot`

# Documentation

[Nupic Wiki](https://github.com/numenta/nupic/wiki)
