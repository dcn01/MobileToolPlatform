# -*- coding: utf-8 -*-
from app.api_v1_2.controller.core.adb import AndroidUtils
from app.api_v1_2.domain.runtime_infos import Runtime


class AppRuntime(object):

    def __init__(self):
        self.android = AndroidUtils()
        self.runtime = Runtime()

    def get_infos(self, sno):
        if sno is None or sno == "":
            return None

        if self.android.device_state(sno) != 'device':
            # self.runtime.__setattr__('unconnect', None)
            # return self.runtime
            return None
        self.runtime.curt_pkg = self.android.current_package_name(sno)

        self.runtime.curt_act = self.android.current_activity(sno)

        if self.runtime.curt_pkg is not None and self.runtime.curt_pkg != '':
            self.runtime.app_permission = self.android.app_permission_dict(sno, self.runtime.curt_pkg)

        self.runtime.screen_status = self.android.is_screen_locked(sno)

        return self.runtime
