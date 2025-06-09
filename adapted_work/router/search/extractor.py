from sqlmodel import func, select

from adapted_work.database.tables import Community, Jobs
from adapted_work.router.search.schema_model import JobItem


def get_total_jobs(community, session):
    """Get all jobs."""
    query = select(func.count(Jobs.id)).join(
        Community, Community.id == Jobs.id_community
    )

    if community:
        query = query.where(Community.name == community)

    count = session.exec(query).first()
    return count


def parse_job_item(result):
    """Parse jobs."""
    jobs = []
    for res in result:
        job = JobItem(
            title=res.title,
            specialty=res.specialty,
            community=res.community,
            disability_vacancies=res.disability_vacancies,
            pred_disability=res.pred_disability,
            link=res.link,
            date=res.date,
        )
        jobs.append(job)

    return jobs


def get_searched_data(size, offset, community, order_by, session):
    """Get search jobs."""
    query = (
        select(
            Jobs.title.label("title"),
            Jobs.specialty.label("specialty"),
            Jobs.disability_vacancies.label("disability_vacancies"),
            Community.name.label("community"),
            Jobs.ext_url.label("link"),
            Jobs.pred_disability.label("pred_disability"),
            Jobs.saved_date.label("date"),
        )
        .join(Community, Community.id == Jobs.id_community)
        .order_by(order_by)
        .limit(size)
        .offset(offset)
    )

    if community:
        query = query.where(Community.name == community)

    result = session.exec(query).all()

    jobs = parse_job_item(result)
    return jobs
