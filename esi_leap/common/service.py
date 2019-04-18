from oslo_db import options as db_options
from oslo_log import log
from oslo_service import service

import esi_leap.conf
from esi_leap import objects
from esi_leap import version

CONF = esi_leap.conf.CONF


def prepare_service(argv=None, default_config_files=None):
    argv = [] if argv is None else argv
    log.register_options(CONF)
    CONF(argv[1:],
         project='esi-leap',
         version=version.version_info.release_string(),
         default_config_files=default_config_files)
    db_options.set_defaults(CONF)
    log.setup(CONF, 'esi-leap')
    objects.register_all()


def process_launcher():
    return service.ProcessLauncher(CONF, restart_method='mutate')
