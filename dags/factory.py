# 'airflow' word is required for the dagbag to parse this file
import logging
import os

import yaml
from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger(__file__)


environment = Environment(loader=FileSystemLoader("templates"))
logger.info(environment.list_templates())
for filename in os.listdir("dags/"):
    if filename.endswith("_dag.yaml"):
        logger.info("creating DAG from %s config", filename)
        with open(f"dags/{filename}", "r", encoding="utf-8") as config_file:
            config = yaml.safe_load(config_file)
            template_name = config.pop("template")
            template = environment.get_template(template_name)
            dag_content = template.render(**config["dag"], **config["tasks"])
            dag_id = config["dag"]["dag_id"]
            with open(f"dags/{dag_id}.py", mode="w", encoding="utf-8") as dag_file:
                dag_file.write(dag_content)
            logger.info(
                "DAG %s created from %s template",
                dag_id,
                template_name,
            )
