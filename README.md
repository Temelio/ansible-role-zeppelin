# zeppelin

[![Build Status](https://travis-ci.org/Temelio/ansible-role-zeppelin.svg?branch=master)](https://travis-ci.org/Temelio/ansible-role-zeppelin)

Install zeppelin package.

## Requirements

This role requires Ansible 2.0 or higher,
and platform requirements are listed in the metadata file.

## Testing

This role use [Molecule](https://github.com/metacloud/molecule/) to run tests.

Locally, you can run tests on Docker (default driver) or Vagrant.
Travis run tests using Docker driver only.

Currently, tests are done on:
- Ubuntu Trusty
- Ubuntu Xenial

and use:
- Ansible 2.0.x
- Ansible 2.1.x
- Ansible 2.2.x
- Ansible 2.3.x

### Running tests

#### Using Docker driver

```
$ tox
```

#### Using Vagrant driver

```
$ MOLECULE_DRIVER=vagrant tox
```

## Role Variables

### Default role variables

``` yaml
# Installation variables
#------------------------------------------------------------------------------

# Package variables
zeppelin_version: '0.7.2'
zeppelin_package: "zeppelin-{{ zeppelin_version }}-bin-all"
zeppelin_package_filename: "{{ zeppelin_package }}.tgz"
zeppelin_download_url: "http://mirrors.standaloneinstaller.com/apache/zeppelin/zeppelin-{{ zeppelin_version }}/{{ zeppelin_package_filename }}"

# Installation folder
zeppelin_root_dir:
  path: "{{ zeppelin_user.home | default('/var/lib/zeppelin') }}"
  user: "{{ zeppelin_user.name }}"
  group: "{{ zeppelin_group.name }}"
  mode: '0750'

# Log folder
zeppelin_log_dir:
  path: '/var/log/zeppelin'
  user: "{{ zeppelin_user.name }}"
  group: "{{ zeppelin_group.name }}"
  mode: '0750'

# PID folder
zeppelin_pid_dir:
  path: '/var/run/zeppelin'
  user: "{{ zeppelin_user.name }}"
  group: "{{ zeppelin_group.name }}"
  mode: '0750'

# User management
zeppelin_group:
  name: 'zeppelin'
zeppelin_user:
  name: 'zeppelin'
  home: '/var/lib/zeppelin'


# Service management
#------------------------------------------------------------------------------

zeppelin_service_description: 'Apache Zeppelin'
zeppelin_service_name: 'zeppelin'
zeppelin_service_state: 'started'
zeppelin_service_enabled: True

# Systemd
zeppelin_service_systemd:
  restart: 'on-failure'
  restart_sec: 1
  wanted_by: 'multi-user.target'


# Configuration - zeppelin-env.sh
#------------------------------------------------------------------------------

zeppelin_environment_items:
  - name: 'ZEPPELIN_LOG_DIR'
    value: "{{ zeppelin_log_dir.path }}"
  - name: 'ZEPPELIN_PID_DIR'
    value: "{{ zeppelin_pid_dir.path }}"


# Configuration - shiro.ini
#------------------------------------------------------------------------------

# Possible values for auth_realm:
#   - active_directory
#   - ldap
#   - pam
#   - zeppelin_hub
zeppelin_shiro: "{{ _zeppelin_shiro }}"
zeppelin_shiro_enabled: False

_zeppelin_shiro:
  auth_realm: None
  global_session_timeout: 86400000
  realms:
    active_directory:
      options: []
    ldap:
      options: []
    pam:
      options:
    service: 'sshd'
    zeppelin_hub:
      options:
        url: 'https://www.zeppelinhub.com'
  roles: []
  user_caching: False
  users: []
  urls:
    - url: '/**'
      permissions: 'authc'


# Configuration - zeppelin-site.xml
#------------------------------------------------------------------------------

# Storage management
# Possible_choices:
#   * s3
#   * azure
#   * local_fs
#   * zeppelin_hub
#   * local_git
zeppelin_storage: 'local_git'

zeppelin_config: "{{ _zeppelin_default_config }}"

_zeppelin_default_config:
  anonymous:
    allowed: True
  dep:
    localrepo: 'local-repo'
  interpreter:
    connect:
      timeout: 30000
    dep:
      mvnRepo: 'http://repo1.maven.org/maven2/'
    dir: 'interpreter'
    group:
      order:
        - 'spark'
        - 'md'
        - 'angular'
        - 'sh'
        - 'livy'
        - 'alluxio'
        - 'file'
        - 'psql'
        - 'flink'
        - 'python'
        - 'ignite'
        - 'lens'
        - 'cassandra'
        - 'geode'
        - 'kylin'
        - 'elasticsearch'
        - 'scalding'
        - 'jdbc'
        - 'hbase'
        - 'bigquery'
        - 'beam'
    localRepo: 'local-repo'
    output:
      limit: 102400
  interpreters:
    - 'org.apache.zeppelin.spark.SparkInterpreter'
    - 'org.apache.zeppelin.spark.PySparkInterpreter'
    - 'org.apache.zeppelin.rinterpreter.RRepl'
    - 'org.apache.zeppelin.rinterpreter.KnitR'
    - 'org.apache.zeppelin.spark.SparkRInterpreter'
    - 'org.apache.zeppelin.spark.SparkSqlInterpreter'
    - 'org.apache.zeppelin.spark.DepInterpreter'
    - 'org.apache.zeppelin.markdown.Markdown'
    - 'org.apache.zeppelin.angular.AngularInterpreter'
    - 'org.apache.zeppelin.shell.ShellInterpreter'
    - 'org.apache.zeppelin.file.HDFSFileInterpreter'
    - 'org.apache.zeppelin.flink.FlinkInterpreter'
    - 'org.apache.zeppelin.python.PythonInterpreter'
    - 'org.apache.zeppelin.python.PythonInterpreterPandasSql'
    - 'org.apache.zeppelin.python.PythonCondaInterpreter'
    - 'org.apache.zeppelin.python.PythonDockerInterpreter'
    - 'org.apache.zeppelin.lens.LensInterpreter'
    - 'org.apache.zeppelin.ignite.IgniteInterpreter'
    - 'org.apache.zeppelin.ignite.IgniteSqlInterpreter'
    - 'org.apache.zeppelin.cassandra.CassandraInterpreter'
    - 'org.apache.zeppelin.geode.GeodeOqlInterpreter'
    - 'org.apache.zeppelin.postgresql.PostgreSqlInterpreter'
    - 'org.apache.zeppelin.jdbc.JDBCInterpreter'
    - 'org.apache.zeppelin.kylin.KylinInterpreter'
    - 'org.apache.zeppelin.elasticsearch.ElasticsearchInterpreter'
    - 'org.apache.zeppelin.scalding.ScaldingInterpreter'
    - 'org.apache.zeppelin.alluxio.AlluxioInterpreter'
    - 'org.apache.zeppelin.hbase.HbaseInterpreter'
    - 'org.apache.zeppelin.livy.LivySparkInterpreter'
    - 'org.apache.zeppelin.livy.LivyPySparkInterpreter'
    - 'org.apache.zeppelin.livy.LivyPySpark3Interpreter'
    - 'org.apache.zeppelin.livy.LivySparkRInterpreter'
    - 'org.apache.zeppelin.livy.LivySparkSQLInterpreter'
    - 'org.apache.zeppelin.bigquery.BigQueryInterpreter'
    - 'org.apache.zeppelin.beam.BeamInterpreter'
    - 'org.apache.zeppelin.pig.PigInterpreter'
    - 'org.apache.zeppelin.pig.PigQueryInterpreter'
    - 'org.apache.zeppelin.scio.ScioInterpreter'
  helium:
    npm:
      registry: 'http://registry.npmjs.org/'
  server:
    addr: '0.0.0.0'
    allowed:
      origins: '*'
    port: 8080
    ssl:
      port: 8443
    context:
      path: '/'
  war:
    tempdir: 'webapps'
  notebook:
    dir: 'notebook'
    homescreen:
      id: ''
      hide: False
    one:
      way:
        sync: False
    public: True
    storage:
      azure:
        connection_string: 'DefaultEndpointsProtocol=https;AccountName=<accountName>;AccountKey=<accountKey>'
        share: 'zeppelin'
        user: 'user'
        storage_class: 'org.apache.zeppelin.notebook.repo.AzureNotebookRepo'
      local_fs:
        storage_class: 'org.apache.zeppelin.notebook.repo.VFSNotebookRepo'
      local_git:
        storage_class: 'org.apache.zeppelin.notebook.repo.GitNotebookRepo'
      s3:
        user: 'user'
        bucket: 'zeppelin'
        endpoint: 's3.amazonaws.com'
        kmsKeyID: 'AWS-KMS-Key-UUID'
        kmsKeyRegion: 'us-east-1'
        encryptionMaterialsProvider: None
        encrypt_data: False
        storage_class: 'org.apache.zeppelin.notebook.repo.S3NotebookRepo'
      zeppelin_hub:
        storage_class:
          - 'org.apache.zeppelin.notebook.repo.GitNotebookRepo'
          - 'org.apache.zeppelin.notebook.repo.zeppelinhub.ZeppelinHubRepo'
  ssl:
    client:
      auth: False
    key:
      manager:
        password: 'change me'
    keystore:
      path: 'keystore'
      password: 'change me'
      type: 'JKS'
    truststore:
      path: 'truststore'
      password: 'change me'
      type: 'JKS'
    use_ssl: False
  websocket:
    max:
      text:
        message:
          size: 1024000
```

## Dependencies

None

## Example Playbook

``` yaml
- hosts: servers
  roles:
    - { role: Temelio.zeppelin }
```

## License

MIT

## Author Information

Alexandre Chaussier (for Temelio company)
- http://www.temelio.com
- alexandre.chaussier [at] temelio.com
