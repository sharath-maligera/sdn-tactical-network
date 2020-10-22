from enum import Enum
from sqlalchemy import (Column, ForeignKey, Integer, String, create_engine,
                        Float, Boolean)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class QoSSwitch(Base):
    """
    Class to represent a switch.
    """
    __tablename__ = "switch"

    dpid = Column(Integer, primary_key=True)


class QoSPort(Base):
    """
    Class to represent a port.
    """
    __tablename__ = "port"

    id = Column(Integer, primary_key=True, autoincrement=True)
    switch = Column(Integer, ForeignKey("switch.dpid"))
    port_no = Column(Integer)


class QoSLink(Base):
    """
    Class to represent a link between two switch ports.
    """
    __tablename__ = "link"

    id = Column(Integer, primary_key=True, autoincrement=True)
    src = Column(ForeignKey("port.switch"))
    dst = Column(ForeignKey("port.switch"), nullable=True)
    bandwidth = Column(Integer)


class QoSReservation(Base):
    """
    Class to represent a bandwidth allocation.
    """
    __tablename__ = 'reservation'

    id = Column(Integer, primary_key=True, autoincrement=True)
    src = Column(String)
    dst = Column(String)
    bw = Column(Integer)
    mpls_label = Column(Integer)
    in_port = Column(Integer, ForeignKey("port.id"))
    out_port = Column(Integer, ForeignKey("port.id"))


class QoSQueue(Base):
    """
    Class to represent a qos port queue.
    """
    __tablename__ = "queue"

    id = Column(Integer, primary_key=True, autoincrement=True)
    port = Column(Integer, ForeignKey('port.id'))
    queue_id = Column(Integer)
    max_rate = Column(Integer, nullable=True)
    min_rate = Column(Integer, nullable=True)


class QoSPortReservation(Base):
    """
    Class to represent an allocation for a specific port.
    """
    __tablename__ = "port_reservation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    port = Column(Integer, ForeignKey("port.id"))
    reservation = Column(Integer, ForeignKey("reservation.id"))


class QoSHost(Base):
    """
    Class to represent a host
    """
    __tablename__ = "host"

    id = Column(Integer, primary_key=True, autoincrement=True)
    mac = Column(String)
    ip = Column(String, nullable=True)
    port = Column(ForeignKey("port.id"))
