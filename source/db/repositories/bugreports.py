from typing import Optional
from sqlalchemy import select, exists

from source.db import tables
from source.db.base import db
from source.models.bugreport import BugReportInDb, AddBugReportInDb


class BugReportsRep:
    @staticmethod
    async def add(bug_report: AddBugReportInDb) -> BugReportInDb:
        q = tables.bug_reports.insert(bug_report.dict()).returning(tables.bug_reports)
        res = await db.fetch_one(q)
        return BugReportInDb.parse_obj(res)

    @staticmethod
    async def all() -> list[BugReportInDb]:
        q = tables.bug_reports.select()
        res = await db.fetch_all(q)
        return [BugReportInDb.parse_obj(d) for d in res]

    @staticmethod
    async def all_done() -> list[BugReportInDb]:
        q = tables.bug_reports.select().where(tables.bug_reports.c.is_done == True)
        res = await db.fetch_all(q)
        return [BugReportInDb.parse_obj(d) for d in res]

    @staticmethod
    async def all_not_done() -> list[BugReportInDb]:
        q = tables.bug_reports.select().where(tables.bug_reports.c.is_done == False)
        res = await db.fetch_all(q)
        return [BugReportInDb.parse_obj(d) for d in res]

    @staticmethod
    async def all_by_user_id(user_id: int) -> list[BugReportInDb]:
        q = tables.bug_reports.select().where(tables.bug_reports.c.user_id == user_id)
        res = await db.fetch_all(q)
        return [BugReportInDb.parse_obj(d) for d in res]

    @staticmethod
    async def all_done_by_user_id(user_id: int) -> list[BugReportInDb]:
        q = tables.bug_reports.select().where(tables.bug_reports.c.user_id == user_id and
                                              tables.bug_reports.c.is_done == True)
        res = await db.fetch_all(q)
        return [BugReportInDb.parse_obj(d) for d in res]
