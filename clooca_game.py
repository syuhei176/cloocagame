# coding: utf-8
"""
"""

from flask import Flask, url_for, render_template, session, request, make_response, redirect
import sys
import os
import zipfile
import json
import md5
import MySQLdb
import config
sys.path.append(config.CLOOCA_MODULE)
from game import RegisterService
from game import DashboardService
from game import AdminService
from game import ProjectService
from game import MetaModelService
from core import CoreService
from core import UserService
from game import ModelCompiler
from core import FileService
from core import GroupService
from core import TemplateService
from mvcs import CommitService
from mvcs import UpdateServiceJSON
from mvcs import RepositoryService
from mvcs import mvcs
from shinshu import compile_server

app = Flask(__name__)

#トップページ

"""
id:1
visibillity public
"""
@app.route('/')
@app.route('/top')
def index():
    if 'user' in session:
        return render_template('/game/top.html', loggedin=True, user=json.dumps(session['user']))
    return render_template('/game/top.html', loggedin=False, user=json.dumps(None))

"""
id:2
visibillity public
"""
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('/game/dashboard.html', loggedin=True, user=json.dumps(session['user']))
    return render_template('/game/dashboard.html', loggedin=False, user=json.dumps(None))

"""
id:2
visibillity public
"""
@app.route('/dashboard/<game_type>')
def dashboard_game(game_type):
    if 'user' in session:
        return render_template('/game/dashboard_game.html', loggedin=True, user=json.dumps(session['user']), game_type=game_type)
    return render_template('/game/dashboard.html', loggedin=False, user=json.dumps(None))


"""
id:3
visibillity public
"""
@app.route('/editor')
def editor():
    return render_template('/game/editor.html')

"""
id:4
visibillity public
"""
@app.route('/battle/<game_type>')
def battle(game_type):
    return render_template('/game/battle.html', game_type=game_type)



"""
id:4
visibillity public
"""
@app.route('/price')
def price():
    return render_template('price.html')

"""
id:5
visibillity public
"""
@app.route('/contact')
def contact():
    return render_template('contact.html')

#登録、ログイン

"""
id:10
visibillity public
"""
@app.route('/reg', methods=['GET'])
def reg_view():
    return render_template('/game/reg.html')

"""
id:11
visibillity public
"""
@app.route('/reg-to', methods=['POST'])
def reg():
    return json.dumps(RegisterService.Register(request.form['username'], request.form['password'], request.form['email']))

"""
id:12
visibillity public
"""
@app.route('/confirm/<key>', methods=['GET'])
def confirm(key):
    if 'user' in session:
        if RegisterService.EnableEmail(session['user'], key):
            return render_template('/game/confirm.html', param=True)
        else:
            return render_template('/game/confirm.html', param=False)
    else:
        return redirect(url_for('login_view'))

"""
id:15
"""
@app.route('/login', methods=['GET'])
def login_view():
    if 'user' in session:
        return redirect('/dashboard')
    else:
        return render_template('/game/login.html')

"""
id:16
"""
@app.route('/login-to', methods=['POST'])
def login():
    user = RegisterService.Login(request.form['username'], request.form['password'])
    if not user == None and 'permanent' in request.form:
        session.permanent = True
    return json.dumps(user)

"""
id:17
"""
@app.route('/logout')
def logout():
    # remove the username from the session if its there
    session.pop('user', None)
    return redirect(url_for('index'))

"""
id:18
"""
@app.route('/get-userinfo')
def get_userinfo():
    if 'user' in session:
        user = UserService.getUserInfo(session['user'])
    return json.dumps(user)

"""
id:19
"""
@app.route('/update-userinfo')
def update_userinfo():
    if 'user' in session:
        user = UserService.updateUserInfo(session['user'])
    return json.dumps(user)



@app.route('/admin')
def admin():
    if 'user' in session:
        return render_template('/game/admin.html', user=json.dumps(session['user']))
    return redirect(url_for('login_view'))

"""
id:20
visibillity editor,wb
"""
@app.route('/mypage')
def mypage():
    if 'user' in session:
        if session['user']['license_type'] == 'free':
            return render_template('mypage_editor.html', user=json.dumps(session['user']))
        if session['user']['license_type'] == 'wb':
            return render_template('mypage_wb.html', user=json.dumps(session['user']))
        if session['user']['license_type'] == 'group':
            return render_template('mypage_wb.html', user=json.dumps(session['user']))
    return redirect(url_for('login_view'))

@app.route('/mycharacters/<game_type>', methods=['GET'])
def mycharacters(game_type):
    if 'user' in session:
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        myprojects = DashboardService.getMyCharacters(connect, session['user'], game_type)
        connect.close()
        return json.dumps(myprojects)
    return 'false'

@app.route('/characters', methods=['GET'])
def characters():
    if 'user' in session:
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        myprojects = DashboardService.getCharacters(connect, session['user'])
        connect.close()
        return json.dumps(myprojects)
    return 'false'


@app.route('/create-chara', methods=['POST'])
def create_chara():
    if 'user' in session:
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        myprojects = DashboardService.createCharacter(connect, session['user'], request.form['name'], request.form['game_type'])
        connect.close()
        return json.dumps(myprojects)
    return 'false'

@app.route('/gen-chara', methods=['POST'])
def gen_chara():
    if 'user' in session:
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        result = DashboardService.genTactics(connect, session['user'], request.form['id'])
        connect.close()
        return json.dumps(result)
    return 'false'

@app.route('/myresults', methods=['POST'])
def myresults():
    if 'user' in session:
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        myprojects = DashboardService.getMyResultsSummary(connect, session['user'], request.form['game_type'])
        connect.close()
        return json.dumps(myprojects)
    return 'null'

@app.route('/insert-result', methods=['POST'])
def insert_result():
    if 'user' in session:
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        myprojects = DashboardService.insertBattleResult(connect, request.form['game_type'], session['user'], request.form['counter'],  request.form['result'])
        connect.close()
        return json.dumps(myprojects)
    return 'false'


"""
id:21
visibillity editor,wb
"""
@app.route('/myprojects', methods=['GET'])
def project_list():
    if 'user' in session:
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        myprojects = ProjectService.loadMyOwnProjectList(session['user'], connect)
        mytools = MetaModelService.loadMyAllMetaModelList(session['user'], connect)
        connect.close()
        for p in myprojects:
            for t in mytools:
                if p['meta_id'] == t['id']:
                    p['tool_id'] = t['id']
                    p['tool_name'] = t['name']
        return json.dumps(myprojects)
    return 'false'

"""
id:22
for editor license
for wb license
"""
@app.route('/mytools', methods=['GET','POST'])
def mytools():
    if 'user' in session:
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        mytools = MetaModelService.loadMyTools(session['user'], connect)
        connect.close()
        return json.dumps(mytools)
    return 'false'

"""
id:23
for wb license
"""
@app.route('/mywbs', methods=['GET','POST'])
def mywbs():
    if 'user' in session:
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        mydevtools = MetaModelService.loadMyAllMetaModelList(session['user'], connect)
        connect.close()
        return json.dumps(mydevtools)
    return 'false'

"""
id:24
for wb license
"""
@app.route('/mytools-wbs', methods=['GET','POST'])
def mytools_wbs():
    if 'user' in session:
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        mydevtools = MetaModelService.loadMyAllMetaModelList(session['user'], connect)
        mytools = MetaModelService.loadMyTools(session['user'], connect)
        connect.close()
        return json.dumps(reduce(lambda a,b: a+b, [mydevtools,mytools],[]))
    return 'false'

"""
id:25
プロジェクト作成する。
"""
@app.route('/createp', methods=['POST'])
def createp():
    if 'user' in session:
        sample = False
        if 'sample' in request.form:
            sample = True
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        if 'group' in session['user']:
            project = ProjectService.createProject(connect,
                                                       session['user'],
                                                       request.form['name'],
                                                       request.form['xml'],
                                                       request.form['metamodel_id'],
                                                       group_id=session['user']['group']['id'],
                                                       _is_sample=sample)
            connect.close()
            return json.dumps(project)
        else:
            project = ProjectService.createProject(connect, session['user'], request.form['name'], request.form['xml'], request.form['metamodel_id'],_is_sample=sample)
            connect.close()
            return json.dumps(project)
    return 'false'

"""
id:26
ツールを作成する
"""
@app.route('/createm', methods=['POST'])
def createm():
    if 'user' in session:
        if 'group' in session['user']:
            project = MetaModelService.createMetaModel(session['user'], request.form['name'], request.form['xml'], request.form['visibillity'], group_id=session['user']['group']['id'])
            return json.dumps(project)
        else:
            project = MetaModelService.createMetaModel(session['user'], request.form['name'], request.form['xml'], request.form['visibillity'], group_id=0)
            return json.dumps(project)
    return 'false'

"""
id:27
"""
@app.route('/deletep', methods=['POST'])
def deletep():
    if 'user' in session:
        result = ProjectService.deleteProject(session['user'], request.form['pid'])
        return json.dumps(result)
    else:
        return 'false'

"""
id:28
"""
@app.route('/deletem', methods=['POST'])
def deletem():
    if 'user' in session:
        result = MetaModelService.deleteMetaModel(session['user'], request.form['id'])
        return json.dumps(result)
    else:
        return 'false'

"""
エディタ
"""
"""
id:30
"""
@app.route('/tactics-editor/<pid>')
def tactics_editor(pid):
    if 'user' in session:
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        result = DashboardService.getMyCharacter(connect, session['user'], pid)
        connect.close()
        return render_template('/game/tactics_editor.html', pid=pid, game_type=result['game_type'])
    else:
        return redirect(url_for('login_view'))
        
@app.route('/tactics-editor-frame/<pid>')
def tactics_editor_frame(pid):
    if 'user' in session:
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        result = ProjectService.loadProject(connect, session['user'], pid)
        connect.close()
        if not result == None:
            return render_template('/game/tactics_editor_frame.html', userinfo=json.dumps(session['user']), project=json.dumps(result))
    else:
        return redirect(url_for('login_view'))
    return render_template('request_deny.html')



@app.route('/editor/<pid>')
def editor(pid):
    if 'user' in session:
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        result = ProjectService.loadProject(connect, session['user'], pid)
        connect.close()
        if not result == None:
            return render_template('editorjs.html', userinfo=json.dumps(session['user']), project=json.dumps(result))
    else:
        return redirect(url_for('login_view'))
    return render_template('request_deny.html')

"""
id:31
"""
@app.route('/psave', methods=['POST'])
def psave():
    return json.dumps(ProjectService.saveProject(session['user'], request.form['pid'], request.form['xml']))

"""
id:32
"""
@app.route('/gen', methods=['POST'])
def gen():
    if 'user' in session:
        generator = ModelCompiler.BaseGenerator()
        mes = generator.GenerateCode(session['user'], int(request.form['pid']), request.form['target']);
        return json.dumps(mes)
    else:
        return 'false'
"""
id:33
"""
@app.route('/download/<pid>', methods=['GET'])
def download(pid):
    if 'user' in session:
        user = session['user']
#        target = request.form['target']
#        generator = ModelCompiler.BaseGenerator()
#        mes = generator.GenerateCode(user, int(pid), target);
        project_id = pid;
        userpath = config.CLOOCA_MODULE+'/out/' + user['uname']
        projectpath = userpath + '/p' + project_id
        filepath = projectpath + '/p' + project_id + '.zip'
        if os.path.exists(projectpath) == True:
            if os.path.exists(filepath) == True:
                os.remove(filepath)
            zip = zipfile.ZipFile(filepath, 'w', zipfile.ZIP_DEFLATED)
            filelist=os.listdir(projectpath)
            for n in range(len(filelist)):
                if not filelist[n].encode('ascii') == 'p' + project_id+'.zip':
                    zip.write(projectpath + '/' + filelist[n].encode('ascii'), filelist[n].encode('ascii'))
            zip.close()
            f = open(filepath, 'rb')
            content = f.read()
            os.remove(filepath)
            resp = make_response(content)
            resp.headers['Content-type'] = 'application/octet-stream;'
            resp.headers['Content-Disposition'] = 'attachment; filename=p'+project_id+'.zip;'
            return resp
    return render_template('request_deny.html')


"""
id:34
"""
@app.route('/run', methods=['POST'])
def run():
    if 'user' in session:
        pass

"""
id:35
"""
@app.route('/deploy', methods=['POST'])
def deploy():
    if 'user' in session:
        pass

"""
id:36
"""
@app.route('/import', methods=['POST'])
def import_project():
    if 'user' in session:
        pass

"""
id:37
"""
@app.route('/export', methods=['POST'])
def export_project():
    if 'user' in session:
        pass

"""
id:40
"""
@app.route('/workbench/<id>')
def workbenchjs(id=None):
    if 'user' in session:
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        toolinfo = AdminService.loadMetaModel(connect, session['user'], id)
        connect.close();
        return render_template('workbenchjs.html', toolinfo=json.dumps(toolinfo))
    return redirect(url_for('login_view'))

"""
id:41
"""
@app.route('/wb/save', methods=['POST'])
def wb_save():
    return json.dumps(MetaModelService.saveMetaModel(session['user'], request.form['id'], request.form['xml']))

"""
id:42
"""
@app.route('/wb/preview/<id>')
def wb_preview(id):
    if 'user' in session:
        result = {}
        result['id'] = None
        result['name'] = 'preview'
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        result['xml'] = MetaModelService.loadSample(connect, session['user'], id)
        result['metamodel_id'] = id
        result['rep_id'] = None
        result['group_id'] = None
        result['metamodel'] = MetaModelService.loadMetaModel(connect, session['user'], id)
        connect.close()
        result['group'] = {}
        result['group']['service'] = 'free'
        return render_template('preview.html', project = json.dumps(result))
    else:
        return redirect(url_for('login_view'))
    return render_template('request_deny.html')

"""
id:43
"""
@app.route('/template/tree', methods=['POST'])
def temp_tree():
    if 'user' in session:
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        result = TemplateService.tree(request.form['id'], connect)
        connect.close()
#        result = FileService.GetFileTree(session['user'], request.form['id'])
        return json.dumps(result)

"""
id:44
"""
@app.route('/template/new', methods=['POST'])
def temp_new():
    if 'user' in session:
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        result = TemplateService.create(request.form['id'], request.form['fname'], request.form['path'], connect)
        connect.close()
        return json.dumps(result)

"""
id:45
"""
@app.route('/template/save', methods=['POST'])
def temp_save():
    if 'user' in session:
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        result = TemplateService.save(int(request.form['id']), request.form['fname'], request.form['target'], request.form['content'], connect)
        connect.close()
        return json.dumps(result)

"""
id:46
"""
@app.route('/template/del', methods=['POST'])
def temp_del():
    if 'user' in session:
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        result = TemplateService.delete(int(request.form['id']), request.form['fname'], request.form['target'], connect)
        connect.close()
        return json.dumps(result)

@app.route('/wb/import', methods=['POST'])
def wb_import():
    if 'user' in session:
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        result = TemplateService.Import(request.form['id'], request.form['text'], connect)
        connect.close()
        return json.dumps(result)

@app.route('/wb/export/<id>', methods=['GET'])
def wb_export(id):
    if 'user' in session:
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        result = TemplateService.Export(id, connect)
        connect.close()
        return result

"""
group
"""

"""
"""
@app.route('/login/<key>', methods=['GET','POST'])
def login_to_group_view(key):
    if request.method == 'GET':
        if 'user' in session and 'group' in session['user'] and session['user']['group']['key'] == key:
            return redirect('/group/'+key)
        else:
            connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
            group = GroupService.getGroupByKey(key, connect)
            connect.close()
            return render_template('login_to_group.html', group=group)
    elif request.method == 'POST':
        result = UserService.LoginToGroup(request.form['username'], request.form['password'], key)
        return json.dumps(result)
    else:
        return render_template('login_to_group.html', group=group)

"""
id:52
"""
@app.route('/group/<group_key>')
def group_dashboard(group_key):
    if 'group' in session and session['group']['key'] == group_key:
        if session['user']['role'] == 0:
            return render_template('mypage_group.html', user=json.dumps(session['user']))
        elif session['user']['role'] == 1:
            return render_template('mypage_group.html', user=json.dumps(session['user']))
        elif session['user']['role'] == 2:
            return render_template('mypage_group.html', user=json.dumps(session['user']))
    else:
        return redirect('/login/'+group_key)
        """
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        cur = connect.cursor()
        cur.execute('SELECT group_id,role FROM JoinInfo WHERE user_id=%s AND group_id=%s;', (session['user']['id'], id, ))
        rows = cur.fetchall()
        cur.close()
        if not len(rows) == 0:
            joinInfo = {}
            joinInfo['id'] = int(id)
            joinInfo['role'] = int(rows[0][1])
            if joinInfo['role'] == 0:
                return render_template('dashboard.html',
                                       loggedin = True,
                                       username = session['user']['uname'],
                                       mymetamodel = json.dumps(MetaModelService.loadMyMetaModelList(session['user'], id, connect)),
                                       myproject = json.dumps(ProjectService.loadMyProjectList(session['user'], id, connect)),
                                       metamodels = json.dumps(MetaModelService.loadMetaModelList(session['user'], id, connect)),
                                       group = GroupService.getGroup(session['user'], joinInfo['id'], connect),
                                       group_id = joinInfo['id'])
            elif joinInfo['role'] == 1:
                return render_template('dashboard1.html',
                                       loggedin = True,
                                       username = session['user']['uname'],
                                       mymetamodel = json.dumps(MetaModelService.loadMyMetaModelList(session['user'], id, connect)),
                                       groupmetamodel = json.dumps(MetaModelService.loadGroupMetaModelList(session['user'], id, connect)),
                                       myproject = json.dumps(ProjectService.loadMyProjectList(session['user'], id, connect)),
                                       metamodels = json.dumps(MetaModelService.loadMetaModelList(session['user'], id, connect)),
                                       group = GroupService.getGroup(session['user'], joinInfo['id'], connect),
                                       members = GroupService.getGroupMember(session['user'], joinInfo['id'], connect),
                                       group_id = joinInfo['id'],hash_key = hash(joinInfo['id']))
    else:
        return redirect(url_for('login_view'))
    return render_template('request_deny.html')
"""

"""
id:54
自分がこのグループで開発中のプロジェクト
"""
@app.route('/group/myprojects', methods=['GET'])
def group_myprojects():
    if 'group' in session['user']:
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        result = ProjectService.loadMyProjectList(connect, user=session['user'], group_id=session['user']['group']['id'])
        connect.close()
        return json.dumps(result)
    else:
        return '[]'

"""
id:55
グループのツール
"""
@app.route('/group/tools', methods=['GET','POST'])
def group_tools():
    if 'group' in session['user']:
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        result = MetaModelService.loadGroupMetaModelList(connect, session['user'], session['group']['id'])
        connect.close()
        return json.dumps(result)
    return '[]'

"""
id:56
自分がこのグループで開発中のツール
"""
@app.route('/group/mytools', methods=['GET','POST'])
def group_mytools():
    if 'group' in session['user']:
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        result = MetaModelService.loadMyMetaModelList(connect, session['user'], session['group']['id'])
        connect.close()
        return json.dumps(result)
    return '[]'

@app.route('/group/members', methods=['GET'])
def group_adduser():
    if 'user' in session:
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        result = MetaModelService.loadMyMetaModelList(connect, session['user'], session['group']['id'])
        connect.close()
        return json.dumps(result)
    return 'false'


@app.route('/group/adduser', methods=['POST'])
def group_adduser():
    if 'user' in session:
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        result = MetaModelService.loadMyMetaModelList(connect, session['user'], session['group']['id'])
        connect.close()
        return json.dumps(result)
    return 'false'

@app.route('/group/deluser', methods=['POST'])
def group_deluser():
    if 'user' in session:
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        result = MetaModelService.loadMyMetaModelList(connect, session['user'], session['group']['id'])
        connect.close()
        return json.dumps(result)
    return 'false'

"""
id:59
"""
@app.route('/update-group', methods=['POST'])
def update_group():
    if 'user' in session:
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        result = GroupService.updateGroup(session['user'], request.form['group_id'], request.form['name'].encode('utf-8'), request.form['detail'].encode('utf-8'), request.form['visibillity'], connect)
        connect.close()
        return json.dumps(result)


"""
market
"""

"""
id:60
"""
@app.route('/market/')
def market_top():
    if 'user' in session:
        return render_template('market/top.html', loggedin = True, username = session['user']['uname'])
    return render_template('market/top.html', loggedin = False, username = '')


"""
id:63
for editor license
for wb license
@param tool_id: 
"""
@app.route('/buy-tool', methods=['POST'])
def buy_tool():
    if 'user' in session:
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        connect.close()
        return json.dumps()
    return 'false'

"""
id:64
for wb license
@param metamodel_id: 
"""
@app.route('/sell-tool', methods=['POST'])
def buy_tool():
    if 'user' in session:
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        connect.close()
        return json.dumps()
    return 'false'

def hash(k):
    return md5.new(str((k * 5 + 100001) % 34567)).hexdigest()

@app.route('/member_reg/<gid>/<key>', methods=['GET'])
def member_reg_view(gid,key):
    connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
    group = GroupService.getGroup(None, gid, connect)
    connect.close()
    if group == None or not key == hash(int(gid)):
        return render_template('request_deny.html')
    if 'user' in session:
        return render_template('member_join.html', group_id=gid, group=group)
    else:
        return render_template('member_reg.html', group_id=gid, group=group)

@app.route('/mygroups')
def mygroups(type='js'):
    if 'user' in session and 'joinInfos' in session['user']:
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        resp = render_template('mygroups.html',
                               username = session['user']['uname'],
                               groups = GroupService.getMyGroups(session['user'], connect))
        connect.close()
        return resp
    return redirect(url_for('login_view'))

@app.route('/groups')
def groups():
    if 'user' in session and 'joinInfos' in session['user']:
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        result = GroupService.getComunity(session['user'], connect)
        connect.close()
        for g in result:
            g['url'] = '/member_reg/'+str(g['id'])+'/'+str(hash(g['id']))
        return render_template('groups.html',
                               username = session['user']['uname'],
                               groups = result)
    return redirect(url_for('login_view'))

@app.route('/account')
def account():
    if 'user' in session:
        return render_template('account.html', user = UserService.getUserInfo(session['user']))
    return redirect(url_for('login_view'))

@app.route('/mydb')
def mydb():
    if 'user' in session:
        return CoreService.mydashboard(session['user'])
    return redirect(url_for('login_view'))
    

@app.route('/editorjs/<pid>')
def editorjs(pid):
    if 'user' in session:
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        result = ProjectService.loadProject(session['user'], pid, connect)
        if not result == None:
            gid = int(result['group_id'])
            cur = connect.cursor()
            cur.execute('SELECT GroupInfo.id AS id1,role,name,service FROM GroupInfo INNER JOIN JoinInfo ON GroupInfo.id = JoinInfo.group_id AND JoinInfo.user_id=%s AND group_id=%s;',(session['user']['id'], gid))
            rows = cur.fetchall()
            cur.close()
            connect.close()
            if not len(rows) == 0:
                joinInfo = {}
                joinInfo['id'] = int(rows[0][0])
                joinInfo['role'] = int(rows[0][1])
                joinInfo['name'] = rows[0][2]
                joinInfo['service'] = rows[0][3]
                result['group'] = joinInfo
                return render_template('editorjs.html', pid = pid, project = json.dumps(result))
    else:
        return redirect(url_for('login_view'))
    return render_template('request_deny.html')



@app.route('/create-group', methods=['POST'])
def create_group():
    if 'user' in session:
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        result = GroupService.createGroup(session['user'], request.form['group_name'], connect)
        connect.close()
        return json.dumps(result)

@app.route('/join-group', methods=['POST'])
def join_group():
    if 'user' in session:
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        result = GroupService.joinGroup(session['user'], request.form['group_id'], connect)
        connect.close()
        return json.dumps(result)

@app.route('/update-role', methods=['POST'])
def update_role():
    if 'user' in session:
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        result = GroupService.updateRole(session['user'], request.form['group_id'], request.form['user_id'], request.form['role'], connect)
        connect.close()
        return json.dumps(result)

@app.route('/free-register', methods=['POST'])
def register_free():
    if 'group_id' in request.form:
        return json.dumps(UserService.CreateUser(request.form['username'], request.form['password'], group_id=request.form['group_id']))
    else:
        return json.dumps(UserService.CreateUser(request.form['username'], request.form['password']))

@app.route('/register', methods=['POST'])
def register_admin():
    return json.dumps(UserService.CreateUser(request.form['username'],
                                             request.form['password'],
                                             role=1,
                                             email=request.form['email']))


@app.route('/pload', methods=['POST'])
def pload():
    if 'user' in session:
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        result = ProjectService.loadProject(session['user'], request.form['pid'])
        connect.close()
        for joinInfo in session['user']['joinInfos']:
            if joinInfo['id'] == result['group_id']:
                result['group'] = joinInfo
                return json.dumps(result)
    return 'false'

@app.route('/mload', methods=['POST'])
def mload():
    connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
    project = MetaModelService.loadMetaModel(connect, session['user'], request.form['id'],check=True)
    connect.close()
    return json.dumps(project)

@app.route('/preview-save', methods=['POST'])
def preview_save():
    if not 'user' in session:
        return 'false'
    if not 'id' in request.form:
        return 'false'
    connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
    res = json.dumps(MetaModelService.saveSample(connect,
                                                 session['user'],
                                                   request.form['id'],
                                                   request.form['sample']))
    connect.close()
    return res



@app.route('/metamodel-save', methods=['POST'])
def metamodel_save():
    if not 'user' in session:
        return 'false'
    if not 'id' in request.form:
        return 'false'
    id = request.form['id']
    if 'name' in request.form and 'xml' in request.form and 'visibillity' in request.form:
        return json.dumps(MetaModelService.saveAll(session['user'],
                                                   request.form['id'],
                                                   request.form['name'],
                                                   request.form['xml'],
                                                   request.form['visibillity'],
                                                   request.form['welcome_message']))
#                                                   request.form['targets']))
    if 'name' in request.form:
        pass
    if 'xml' in request.form:
        pass
    if 'visibillity' in request.form:
        pass
    return 'false'
    

@app.route('/tcsave', methods=['POST'])
def tcsave():
    return json.dumps(MetaModelService.saveTempConfig(session['user'], request.form['id'], request.form['tc']))

@app.route('/compile_server/reserve', methods=['POST'])
def compile_server_reserve():
    if 'user' in session:
        return json.dumps(compile_server.reserve(session['user'], request.form['pid'], request.form['pname']))
        
'''
template
'''

@app.route('/template/import', methods=['POST'])
def temp_import():
    if 'user' in session:
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        result = TemplateService.Import(request.form['id'], request.form['text'], connect)
        connect.close()
        return json.dumps(result)

@app.route('/template/export/<id>', methods=['GET'])
def temp_export(id):
    if 'user' in session:
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        result = TemplateService.Export(id, connect)
        connect.close()
        return result

'''
mvcs
'''
@app.route('/mvcs/commit', methods=['POST'])
def commit():
    if 'user' in session:
        resp = mvcs.commit(session['user'], pid=request.form['pid'], comment=request.form['comment'], xml=request.form['xml'])
        return json.dumps(resp)

@app.route('/mvcs/update', methods=['POST'])
def update():
    if 'user' in session:
        resp = mvcs.update(session['user'], pid=request.form['pid'])
        return json.dumps(resp)

@app.route('/mvcs/update_to_version', methods=['POST'])
def update_to_version():
    if 'user' in session:
        resp = mvcs.update_to_version(session['user'], pid=request.form['pid'], version=request.form['version'])
        return json.dumps(resp)

@app.route('/mvcs/checkout', methods=['POST'])
def checkout():
    if 'user' in session:
        resp = mvcs.checkout(session['user'], pid=request.form['pid'], rep_id=request.form['rep_id'])
        return json.dumps(resp)

@app.route('/mvcs/import', methods=['POST'])
def mvcs_import():
    if 'user' in session:
        resp = mvcs.import_to_rep(session['user'], xml=request.form['xml'], rep_id=request.form['rep_id'])
        return json.dumps(resp)

@app.route('/mvcs/export', methods=['POST'])
def mvcs_export():
    if 'user' in session:
        resp = mvcs.export_from_rep(session['user'], pid=request.form['pid'], rep_id=request.form['rep_id'])
        return json.dumps(resp)

@app.route('/mvcs/create_rep', methods=['POST'])
def create_rep():
    if 'user' in session:
        resp = mvcs.create_rep(session['user'], request.form['name'], request.form['group_id'])
        return json.dumps(resp)

@app.route('/mvcs/clear_rep', methods=['POST'])
def clear_rep():
    if 'user' in session:
        resp = mvcs.clear_rep(session['user'], rep_id=request.form['rep_id'])
        return json.dumps(resp)

@app.route('/mvcs/delete_rep', methods=['POST'])
def delete_rep():
    if 'user' in session:
        resp = mvcs.delete_rep(session['user'], rep_id=request.form['rep_id'], group_id=request.form['group_id'])
        return json.dumps(resp)

@app.route('/mvcs/rep_list', methods=['POST'])
def rep_list():
    if 'user' in session:
        resp = mvcs.rep_list(session['user'])
        return json.dumps(resp)

@app.route('/mvcs/ver_list', methods=['POST'])
def ver_list():
    if 'user' in session:
        resp = mvcs.ver_list(session['user'], pid=request.form['pid'])
        return json.dumps(resp)

@app.route('/mvcs/user_rep_list', methods=['POST'])
def user_rep_list():
    if 'user' in session:
        resp = mvcs.user_rep_list(session['user'])
        return json.dumps(resp)

@app.route('/mvcs/group_rep_list', methods=['POST'])
def group_rep_list():
    if 'user' in session:
        resp = mvcs.group_rep_list(request.form['group_id'])
        return json.dumps(resp)

@app.route('/mvcs/gethistory', methods=['POST'])
def gethistory():
    if 'user' in session:
        resp = mvcs.get_history(request.form['pid'])
        return json.dumps(resp)

@app.route('/mvcs/viewer/<id>', methods=['GET'])
def mvcs_viewer(id):
    if 'user' in session:
        resp = RepositoryService.getHistory(id);
        return render_template('rep_view.html', history=resp)
    return redirect(url_for('login_view'))

@app.route('/wb/')
def wb_top():
    if 'user' in session:
        return render_template('wb/top.html', loggedin = True, username = session['user']['uname'])
    return render_template('wb/top.html', loggedin = False, username = '')

@app.route('/wb/dashboard')
def wb_dashboard():
    if 'user' in session:
        connect = MySQLdb.connect(db=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSWD)
        mymetamodels = MetaModelService.loadMyOwnMetaModelList(session['user'], connect)
        connect.close()
        return render_template('wb/dashboard.html',
                               loggedin = True,
                               username = session['user']['uname'],
                               mymetamodels = mymetamodels)
    return redirect(url_for('login_view'))

@app.route('/tool/<id>/')
def tool_top(id):
    if 'user' in session:
        return render_template('tool/top.html', loggedin = True, username = session['user']['uname'])
    return render_template('request_deny.html')

@app.route('/tool/<id>/dashboard')
def tool_top(id):
    if 'user' in session:
        return render_template('tool/dashboard.html', loggedin = True, username = session['user']['uname'])
    return render_template('tool/top.html', loggedin = False, username = '')

@app.route('/tool/<tid>/editor/<pid>')
def tool_top(tid,pid):
    if 'user' in session:
        return render_template('tool/editor.html', loggedin = True, username = session['user']['uname'])
    return render_template('tool/top.html', loggedin = False, username = '')

with app.test_request_context():
    print url_for('index')
    print url_for('login')

#sercret key
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if not app.debug:
    import logging
    from logging import FileHandler
    file_handler = FileHandler(config.CLOOCA_ROOT + '/log.txt')
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)
    
if __name__ == '__main__':
    app.run(debug=True,port=5001)