from batch.jobs.bond_job import run as run_bond_job
from batch.jobs.real_estate_job import run as run_real_estate_job
from batch.jobs.stock_job import run as run_stock_job


def run_all() -> None:
    run_bond_job()
    run_stock_job()
    run_real_estate_job()


if __name__ == "__main__":
    run_all()
