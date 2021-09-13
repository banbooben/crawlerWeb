from sqlalchemy import Column, VARCHAR, Text, BOOLEAN, false, DATETIME, SMALLINT, text

from utils.constant.idea_enum import StateEnum

from .base_entity import BaseEntity


class IdeaEntity(BaseEntity):
    __tablename__ = "t_idea"
    __table_args__ = {"comment": "备忘录表"}

    title = Column(VARCHAR(255), index=True, comment="备忘录标题", server_default="")
    level = Column(SMALLINT(), name="level", comment="状态", server_default=text(str(StateEnum.normal.value)))
    text = Column(Text(), comment="备忘录内容", default="")
    is_done = Column(BOOLEAN(), server_default=false(), comment="是否完成")
    done_at = Column(DATETIME(), comment="完成时间")
