from __future__ import annotations

from collections.abc import Callable

from qtpy import QtCore


def single_shot(parent: QtCore.QObject, msec: int, callback: Callable[[], None]) -> QtCore.QTimer:
    """Start a single-shot timer that is owned by parent.

    In contrast to the static QTimer.singleShot(), the returned timer is a child of
    parent and therefore destroyed together with it. Otherwise a pending callback
    keeps its captured objects (usually the whole window) alive until it fires,
    which never happens without a running event loop.
    """
    timer = QtCore.QTimer(parent)
    timer.setSingleShot(True)
    timer.timeout.connect(callback)
    timer.timeout.connect(timer.deleteLater)
    timer.start(msec)
    return timer
