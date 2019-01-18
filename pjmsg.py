from flask import Flask, render_template, url_for, redirect, request
from db import db
from db.mysql import Project, Module

app = Flask(__name__)
# module: 1:基础应用 2:中台应用 3:系统监控 4:基础设施


@app.route('/<module_id>/<env>/')
def index_env(module_id, env):
    module = Module.query.filter_by(id=module_id).first()
    modules = Module.query.order_by('order').all()
    project = Project.query.filter_by(env=env, moduleId=module_id).order_by('name').all()
    return render_template('index.html', project=project, env=env, modules=modules, module=module)


@app.route('/manager/<module_id>/<env>/')
def back_view(module_id, env):
    module = Module.query.filter_by(id=module_id).first()
    modules = Module.query.order_by('order').all()
    project = Project.query.filter_by(env=env, moduleId=module_id).order_by('name').all()
    return render_template('back_view.html', project=project, env=env, modules=modules, module=module)


@app.route('/manager/edit/<project_id>/')
def back_edit(project_id):
    modules = Module.query.order_by('order').all()
    project_cur = Project.query.filter_by(id=project_id).first()
    project_dev = Project.query.filter_by(name=project_cur.name, env='DEV').first()
    project_fat = Project.query.filter_by(name=project_cur.name, env='FAT').first()
    project_pro = Project.query.filter_by(name=project_cur.name, env='PRO').first()
    return render_template('back_form.html', project_cur=project_cur, project_dev=project_dev,
                           project_fat=project_fat, project_pro=project_pro, modules=modules)


@app.route('/api/modify', methods=['POST'])
def api_modify():
    param = request.form
    project_pro = Project.query.filter_by(id=param['id_pro']).first()
    project_fat = Project.query.filter_by(id=param['id_fat']).first()
    project_dev = Project.query.filter_by(id=param['id_dev']).first()
    if project_pro:
        project_pro.http = param['http_pro']
        project_pro.k8sAddr = param['k8sAddr_pro']
        project_pro.privateAddr = param['privateAddr_pro']
        project_pro.publicAddr = param['publicAddr_pro']
    else:
        project_pro_new = Project()
        project_pro_new.name = param['project_name']
        project_pro_new.env = 'PRO'
        project_pro_new.moduleId = param['module_id']
        project_pro_new.http = param['http_pro']
        project_pro_new.k8sAddr = param['k8sAddr_pro']
        project_pro_new.privateAddr = param['privateAddr_pro']
        project_pro_new.publicAddr = param['publicAddr_pro']
        db.session.add(project_pro_new)
    if project_fat:
        project_fat.http = param['http_fat']
        project_fat.k8sAddr = param['k8sAddr_fat']
        project_fat.privateAddr = param['privateAddr_fat']
        project_fat.publicAddr = param['publicAddr_fat']
    else:
        project_fat_new = Project()
        project_fat_new.name = param['project_name']
        project_fat_new.env = 'FAT'
        project_fat_new.moduleId = param['module_id']
        project_fat_new.http = param['http_fat']
        project_fat_new.k8sAddr = param['k8sAddr_fat']
        project_fat_new.privateAddr = param['privateAddr_fat']
        project_fat_new.publicAddr = param['publicAddr_fat']
        db.session.add(project_fat_new)
    if project_dev:
        project_dev.http = param['http_dev']
        project_dev.k8sAddr = param['k8sAddr_dev']
        project_dev.privateAddr = param['privateAddr_dev']
        project_dev.publicAddr = param['publicAddr_dev']
    else:
        project_dev_new = Project()
        project_dev_new.name = param['project_name']
        project_dev_new.env = 'DEV'
        project_dev_new.moduleId = param['module_id']
        project_dev_new.http = param['http_dev']
        project_dev_new.k8sAddr = param['k8sAddr_dev']
        project_dev_new.privateAddr = param['privateAddr_dev']
        project_dev_new.publicAddr = param['publicAddr_dev']
        db.session.add(project_dev_new)
    db.session.commit()
    return redirect(url_for('back_view', env=param['project_env'], module_id=param['module_id']))


@app.route('/api/add', methods=['POST'])
def api_add():
    param = request.form
    project = Project.query.filter_by(name=param['project_name']).first()
    if project:
        return '项目已存在'
    else:
        project_dev = Project()
        project_dev.name = param['project_name']
        project_dev.moduleId = param['prject_moduleId']
        project_dev.remark = param['project_remark']
        project_dev.env = 'DEV'
        project_dev.http = ''
        db.session.add(project_dev)
        project_fat = Project()
        project_fat.name = param['project_name']
        project_fat.moduleId = param['prject_moduleId']
        project_fat.remark = param['project_remark']
        project_fat.env = 'FAT'
        project_fat.http = ''
        db.session.add(project_fat)
        project_pro = Project()
        project_pro.name = param['project_name']
        project_pro.moduleId = param['prject_moduleId']
        project_pro.remark = param['project_remark']
        project_pro.env = 'PRO'
        project_pro.http = ''
        db.session.add(project_pro)
        db.session.commit()
        return redirect(url_for('back_view', env='DEV', module_id=param['prject_moduleId']))


@app.route('/add')
def back_add():
    modules = Module.query.order_by('order').all()
    return render_template('back_add.html', modules=modules)


@app.route('/api/login', methods=['POST'])
def api_login():
    pwd = request.form['logpass']
    if pwd == 'Jmtop123':
        return redirect(url_for('back_view', env='DEV', module_id=1))
    else:
        return render_template('login.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/manager')
def manager_index():
    return redirect(url_for('back_view', env='DEV', module_id=1))


@app.route('/')
def index():
    return redirect(url_for('index_env', env='DEV', module_id=1))


@app.teardown_request
def shutdown_session(exception=None):
    db.session.remove()
    pass


if __name__ == '__main__':
    app.run()
