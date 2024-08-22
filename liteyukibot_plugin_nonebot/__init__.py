# -*- coding: utf-8 -*-
"""
Copyright (C) 2020-2024 LiteyukiStudio. All Rights Reserved 

@Time    : 2024/8/11 下午5:24
@Author  : snowykami
@Email   : snowykami@outlook.com
@File    : __init__.py.py
@Software: PyCharm
"""

import nonebot
from liteyuki.utils import IS_MAIN_PROCESS
from liteyuki.plugin import PluginMetadata
from .nb_utils import adapter_manager, driver_manager

__plugin_meta__ = PluginMetadata(
    name="NoneBot2启动器",
)


def nb_run(*args, **kwargs):
    """
    初始化NoneBot并运行在子进程
    Args:
        **kwargs:

    Returns:
    """
    # 给子进程传递通道对象

    kwargs.update(kwargs.get("nonebot", {}))  # nonebot配置优先
    nonebot.init(**kwargs)

    driver_manager.init(config=kwargs)
    adapter_manager.init(kwargs)
    adapter_manager.register()

    base_plugin_dir = "liteyukibot_plugin_nonebot.nonebot_plugins."
    nonebot_plugins = ["to_liteyuki"]
    try:
        for plugin in nonebot_plugins:
            nonebot.load_plugin(base_plugin_dir + plugin)
    except Exception as e:
        pass

    nonebot.run()


if IS_MAIN_PROCESS:
    from .dev_reloader import *

    liteyuki = get_bot()


    @liteyuki.on_before_start
    async def start_run_nonebot():
        liteyuki.process_manager.add_target(name="nonebot", target=nb_run, args=(), kwargs=liteyuki.config)
