/* Copyright (C) 2012 Technical Rockstars Co.,Ltd. All Rights Reserved. */function readProject(a){Ext.MessageBox.show({title:'Please wait',msg:'Loading...',progressText:'Initializing...',width:300,progress:true,closable:false,animEl:'mb6'});if(a){g_projectinfo=a;g_metamodel_id=g_projectinfo.metamodel_id;if(g_projectinfo.metamodel.xml==' '||g_projectinfo.metamodel.xml==null||g_projectinfo.metamodel.xml.length==0)g_metamodel=new MetaModel();else g_metamodel=JSON.parse(g_projectinfo.metamodel.xml);metadiagrams_length=0;for(a in g_metamodel.metadiagrams)metadiagrams_length++;if(metadiagrams_length==0){alert("ダイアグラムが一つもありません。");window.close();}g_projectinfo.metamodel.config=JSON.parse(g_projectinfo.metamodel.config);readModel(g_projectinfo.xml);}}function readModel(a){console.log('loaded json string = '+a);if(a=='null'||a==''||a==undefined){g_model=new Model();Ext.MessageBox.hide();Ext.Msg.prompt('ダイアグラム','新規作成',function(a,b){if(a!='cancel'){var c=ModelController.addDiagram(g_metamodel.metadiagram);g_model.root=c.id;var d=g_metamodel.metadiagrams[c.meta_id];if(d.instance_name!=null&&d.instance_name!=undefined){var e=g_metamodel.metaproperties[d.properties[d.instance_name]].id;var f=null;for(var g=0;g<c.properties.length;g++)if(c.properties[g].meta_id==e)f=c.properties[g];g_model.properties[f.children[0]].value=b;}diagram_IdGenerator.setOffset(g_model.root);g_modelExplorer=new ModelExplorer();}},null,false,'');}else{g_model=JSON.parse(a);Ext.MessageBox.hide();g_modelExplorer=new ModelExplorer();}for(var b in g_model.diagrams){obj=g_model.diagrams[b];if(obj==null)continue;if(g_projectinfo.id*10000<=obj.id&&(g_projectinfo.id+1)*10000>obj.id)diagram_IdGenerator.setOffset(obj.id-g_projectinfo.id*10000);}for(var b in g_model.objects){obj=g_model.objects[b];if(obj==null)continue;if(g_projectinfo.id*10000<=obj.id&&(g_projectinfo.id+1)*10000>obj.id)object_IdGenerator.setOffset(obj.id-g_projectinfo.id*10000);}for(var b in g_model.objects){obj=g_model.objects[b];calObjHeight(obj);if(obj.ofd==undefined)obj.ofd={z:0};}for(var b in g_model.relationships){obj=g_model.relationships[b];if(obj==null)continue;if(g_projectinfo.id*10000<=obj.id&&(g_projectinfo.id+1)*10000>obj.id)object_IdGenerator.setOffset(obj.id-g_projectinfo.id*10000);}for(var b in g_model.relationships){obj=g_model.relationships[b];if(obj.rfd==undefined)obj.rfd={z:0};}for(var b in g_model.properties){var c=g_model.properties[b];if(c==null)continue;if(g_projectinfo.id*10000<=c.id&&(g_projectinfo.id+1)*10000>c.id)property_IdGenerator.setOffset(c.id-g_projectinfo.id*10000);}}function showGenerateWindow(){if(g_projectinfo.metamodel.config.editor.generatable){}else{Ext.Msg.alert('ソースコード生成はできません。');return;}var a=null;var b=Ext.create('Ext.data.Store',{fields:['name'],data:g_projectinfo.metamodel.config.targets});var c=Ext.create('Ext.window.Window',{title:'Generate',width:280,height:200,layout:'vbox',items:[{xtype:'combo',fieldLabel:'target',store:b,queryMode:'local',displayField:'name',valueField:'name',listeners:{scope:this,'select':function(b,c,d){a=b.getValue();}}},{xtype:'button',text:'OK',handler:function(){if(a){Generate(g_project_id,a);c.hide();}else Ext.Msg.alert('ターゲットを選択してください。');}}]});c.show();}function showDownloadWindow(){if(g_projectinfo.metamodel.config.editor.generatable){}else{Ext.Msg.alert('ソースコード生成はできません。');return;}var a=null;var b=[];for(var c=0;c<g_projectinfo.metamodel.config.targets.length;c++)if(g_projectinfo.metamodel.config.targets[c].downloadable)b.push(g_projectinfo.metamodel.config.targets[c]);var d=Ext.create('Ext.data.Store',{fields:['name'],data:b});var e=Ext.create('Ext.window.Window',{title:'Download',width:280,height:200,layout:'vbox',items:[{xtype:'combo',fieldLabel:'target',store:d,queryMode:'local',displayField:'name',valueField:'name',listeners:{scope:this,'select':function(b,c,d){a=b.getValue();}}},{xtype:'button',text:'OK',handler:function(){if(a){Generate(g_project_id,a,function(a){if(a)download(g_projectinfo.id);});e.hide();}else Ext.Msg.alert('ターゲットを選択してください。');}}]});e.show();}function showRunWindow(){if(g_projectinfo.metamodel.config.editor.generatable){}else{Ext.Msg.alert('ソースコード生成はできません。');return;}var a=null;var b=[];for(var c=0;c<g_projectinfo.metamodel.config.targets.length;c++)if(g_projectinfo.metamodel.config.targets[c].runnable)b.push(g_projectinfo.metamodel.config.targets[c]);var d=Ext.create('Ext.data.Store',{fields:['name'],data:b});var e=Ext.create('Ext.window.Window',{title:'Run',width:280,height:200,layout:'vbox',items:[{xtype:'combo',fieldLabel:'target',store:d,queryMode:'local',displayField:'name',valueField:'name',listeners:{scope:this,'select':function(b,c,d){a=b.getValue();}}},{xtype:'button',text:'OK',handler:function(){if(a){Generate(g_project_id,a);e.hide();}else Ext.Msg.alert('ターゲットを選択してください。');}}]});e.show();}function showDeployWindow(){if(g_projectinfo.metamodel.config.editor.generatable){}else{Ext.Msg.alert('ソースコード生成はできません。');return;}var a=null;var b=[];for(var c=0;c<g_projectinfo.metamodel.config.targets.length;c++)if(g_projectinfo.metamodel.config.targets[c].deploy)b.push(g_projectinfo.metamodel.config.targets[c]);var d=Ext.create('Ext.data.Store',{fields:['name'],data:b});var e=Ext.create('Ext.window.Window',{title:'Deploy',width:280,height:200,layout:'vbox',items:[{xtype:'combo',fieldLabel:'target',store:d,queryMode:'local',displayField:'name',valueField:'name',listeners:{scope:this,'select':function(b,c,d){a=b.getValue();}}},{xtype:'button',text:'OK',handler:function(){if(a){Generate(g_project_id,a);e.hide();}else Ext.Msg.alert('ターゲットを選択してください。');}}]});e.show();}function commit(){g_model.id=g_projectinfo.id;var a=JSON.stringify(g_model);Ext.Msg.prompt('コミットします。','コメントを書いてください。',function(b,c){if(b!='cancel'){Ext.MessageBox.show({title:'Please wait',msg:'Commit',progressText:'Initializing...',width:300,progress:true,closable:false,animEl:'mb6'});$.post('/mvcs/commit',{pid:g_projectinfo.id,comment:c,xml:a},function(a){if(a){console.log('commit state = '+a);Ext.MessageBox.hide();if(a==1){Ext.MessageBox.alert("コミットステート","成功");update();}else if(a==2)Ext.MessageBox.alert("コミットステート","最新バージョンに更新してください。");else if(a==3)Ext.MessageBox.alert("コミットステート","変更がありません。");}else{Ext.MessageBox.hide();Ext.MessageBox.alert("コミットステート","失敗：リポジトリが存在しないか、チェックアウトしていません。");}},"json");}},null,true,'');}function update(){Ext.MessageBox.show({title:'Please wait',msg:'Update',progressText:'Initializing...',width:300,progress:true,closable:false,animEl:'mb6'});$.post('/mvcs/update',{pid:g_projectinfo.id},function(a){if(a.ret_state==0){console.log('loaded json string = '+a.xml);g_projectinfo.xml=a.xml;readModel(a.xml);g_modelExplorer=new ModelExplorer();Ext.MessageBox.hide();editortabpanel.close();}else{alert('update error');Ext.MessageBox.hide();}},"json");}function update_to_ver(a,b){$.post('/mvcs/update_to_version',{pid:g_projectinfo.id,version:a},function(a){if(a.ret_state==0){console.log('loaded json string = '+a.xml);g_projectinfo.xml=a.xml;readModel(a.xml);g_modelExplorer=new ModelExplorer();Ext.MessageBox.hide();editortabpanel.close();b();}else{alert('update error');Ext.MessageBox.hide();}},"json");}function create_rep(){Ext.Msg.prompt('確認','リポジトリを作成しますか？',function(a,b){if(a!='no'&&b.length!=0)$.post('/mvcs/create_rep',{pid:g_projectinfo.id,name:b,space_key:g_userinfo.space_key},function(a){if(a){}else Ext.Msg.alert('リポジトリの名前が長過ぎます。');},"json");},null,false);}function clear_rep(a){$.post('/mvcs/clear_rep',{rep_id:a},function(a){if(a)console.log('loaded json string = '+a.xml);},"json");}function delete_rep(a,b){$.post('/mvcs/delete_rep',{rep_id:a,group_id:g_projectinfo.group.id},function(a){if(a){console.log('Success');b();}else console.log('Failure');},"json");}function history_view(){$.post('/mvcs/gethistory',{pid:g_projectinfo.id},function(a){if(a){console.log('version\tcomment');for(var b=0;b<a.length;b++)console.log(a[b].version+'\t'+a[b].content);}},"json");}function ver_list(){$.post('/mvcs/ver_list',{pid:g_projectinfo.id},function(a){if(a){console.log('version\tcomment');for(var b=0;b<a.length;b++)console.log(a[b].version+'\t'+a[b].content);}},"json");}function rep_list(){$.post('/mvcs/group_rep_list',{group_id:g_projectinfo.group.id},function(a){if(a){console.log('id\tname\thead_version');for(var b=0;b<a.length;b++)console.log(a[b].id+'\t'+a[b].name+'\t'+a[b].head_version);}},"json");}function checkout(a,b){$.post('/mvcs/checkout',{pid:g_projectinfo.id,rep_id:a},function(a){if(a.ret_state==0){readModel(a.xml);b();}else alert('checkout error');},"json");}function import_to_rep(a,b){g_model.id=g_projectinfo.id;var c=JSON.stringify(g_model);$.post('/mvcs/import',{xml:c,rep_id:a},function(a){if(a==1)b();else alert('checkout error');},"json");}Ext.require(['Ext.panel.*','Ext.toolbar.*','Ext.button.*','Ext.container.ButtonGroup','Ext.layout.container.Table']);function init_clooca(a,b,c){g_editor_option=c;current_editor=null;g_project_id=a.id;g_projectinfo=a;_is_preview=b;readProject(a);Ext.getCmp('menupanel').add(create_menu());Ext.getCmp('centerpanel').add(create_tabs());if(g_editor_option.diagram_open)for(var d in g_model.diagrams)g_modelExplorer.open_diagram(g_model.diagrams[d],g_model.diagrams[d].id);window.onbeforeunload=function(){return "このページから移動しますか？ データは保存されません。";};}function create_tabs(){editortabpanel=new EditorTabPanel();editortabpanel.add(new WelcomeMessageView(),'welcome');return editortabpanel.getPanel();}function create_menu(){var a=false;if(g_projectinfo.metamodel.config.editor.generatable)a=false;else a=true;var b={tbar:[{text:'Edit',iconCls:'add16',menu:[{id:'open',text:'開く',iconCls:'add16',handler:onItemClick},{id:'delete',text:'削除',iconCls:'add16',handler:onItemClick},{id:'deletePoints',text:'ポイントを削除',iconCls:'add16',handler:onItemClick},{id:'diagram',text:'ダイアグラム',iconCls:'add16',handler:onItemClick},{text:'エクスポート',iconCls:'add16',menu:[{id:'png',text:'png',iconCls:'add16',handler:onItemClick},{id:'jpg',text:'jpg',iconCls:'add16',handler:onItemClick}]}],handler:onItemClick},{text:'プロジェクト',iconCls:'add16',menu:[{id:'generate',text:'generate',iconCls:'add16',handler:onProjItemClick,hidden:a},{id:'download',text:'Download',iconCls:'add16',handler:onProjItemClick,hidden:a},{id:'run',text:'Run',iconCls:'add16',handler:onProjItemClick,hidden:a},{id:'deploy',text:'Deploy',iconCls:'add16',handler:onProjItemClick,hidden:a},{id:'pviewer',text:'プロジェクト情報',iconCls:'add16',handler:onProjItemClick}]},'-',{id:'save',text:'保存',iconCls:'add16',handler:onItemClick}]};b.tbar.push({text:'リポジトリ',iconCls:'add16',menu:[{id:'manage_repository',text:'リポジトリ',iconCls:'add16',menu:[{id:'create_rep',text:'リポジトリ作成',iconCls:'add16',handler:onRepItemClick},{id:'clear_rep',text:'リポジトリ削除',iconCls:'add16',handler:onRepItemClick},{id:'import',text:'インポート',iconCls:'add16',handler:onRepItemClick},{id:'checkout',text:'チェックアウト',iconCls:'add16',handler:onRepItemClick}]},{id:'commit',text:'コミット',iconCls:'add16',handler:onRepItemClick},{id:'update',text:'アップデート',iconCls:'add16',handler:onRepItemClick},{id:'update_to_ver',text:'前のバージョンに戻す',iconCls:'add16',handler:onRepItemClick},{id:'history',text:'ヒストリー',iconCls:'add16',handler:onRepItemClick}],handler:onItemClick});return b;}function onItemClick(a){if(a.id=='open')g_modelExplorer.open_selected_diagram();else if(a.id=='exit'){window.opener="dummy";window.open("about:blank","_self").close();}else if(a.id=='save')saveModel(g_project_id);else if(a.id=='diagram')if(current_editor!=null&&current_editor.selected!=null&&g_metamodel.metaobjects[current_editor.selected.meta_id].decomposition!=null&&current_editor.selected.diagram==null)show_setting_diagram_name_window(g_metamodel.metaobjects[current_editor.selected.meta_id].decomposition,function(a){current_editor.selected.diagram=a.id;});else show_create_diagram_window();else if(a.id=='png')current_editor.getImage('png');else if(a.id=='jpg')current_editor.getImage('jpg');else if(a.id=='delete')current_editor.deleteSelected();else if(a.id=='deletePoints')current_editor.deletePoint();else{}}function onFileItemClick(a){if(a.id=='create_rep')create_rep();else if(a.id=='clear_rep')clear_rep();}function onProjItemClick(a){if(a.id=='generate')showGenerateWindow();else if(a.id=='download')showDownloadWindow();else if(a.id=='run')showRunWindow();else if(a.id=='deploy')showDeployWindow();else if(a.text=='genbin')genbin(g_project_id);else if(a.id=='pviewer'){var b=new ProjectInfoViewer();editortabpanel.add(b,'pviewer');}}function onRepItemClick(a){if(a.id=='create_rep')create_rep();else if(a.id=='clear_rep')delete_rep_view();else if(a.id=='checkout')checkoutview();else if(a.id=='commit')commit();else if(a.id=='update'){Ext.MessageBox.confirm("確認","自分の変更とリポジトリをマージさせたい時は、まず保存をしてくださいね。保存していない場合は、「No」を押して、保存してください。　アップデートしますか？",function(a){if(a=="yes")update();else if(a=="no"){}},window);}else if(a.id=='update_to_ver')update_to_ver_view();else if(a.id=='history'){window.open('/mvcs/viewer/'+g_projectinfo.rep_id);$.post('/mvcs/gethistory',{pid:g_projectinfo.id},function(a){for(var b in a.verlist){console.log(a.verlist[b].version,a.verlist[b].content);for(var c=0;c<a.verlist[b].changes.length;c++)console.log(a.verlist[b].changes[c].ver_type+','+a.verlist[b].changes[c].type);}},"json");}else if(a.id=='import')import_to_rep_view();}function onShinshuItemClick(a){if(a.id=='genbin')genbin(g_project_id);}function ModelExplorer(){var a=this;this.selected_diagram=null;var b=[];for(var c in g_model.diagrams)if(g_model.diagrams[c].ve.ver_type!='delete'){var d=g_model.diagrams[c];var e=false;if(d.id==g_model.root)e=true;var f=g_metamodel.metadiagrams[d.meta_id];var g='diagram_'+c;if(f.instance_name!=null&&f.instance_name!=undefined){var h=g_metamodel.metaproperties[f.properties[f.instance_name]].id;var i=null;for(var j=0;j<d.properties.length;j++)if(d.properties[j].meta_id==h)i=d.properties[j];g=g_model.properties[i.children[0]].value;}g+='('+f.name+')';if(e)b.push({id:c,text:g,leaf:true,icon:'/static/images/editor/root_leaf.gif'});else b.push({id:c,text:g,leaf:true});}var k=Ext.create('Ext.data.TreeStore',{root:{expanded:true,children:[{text:"root",expanded:true,children:b}]}});var l=Ext.create('Ext.tree.Panel',{width:240,height:280,store:k,rootVisible:false});l.on('itemdblclick',function(b,c,d,e,f){if(c.data.text!='root'){var g=g_model.diagrams[c.data.id];a.open_diagram(g,c.data.id,c.data.text);}});var m=new Ext.menu.Menu({items:[{id:'delete',text:'削除'},{id:'open',text:'開く'},{id:'change',text:'名前を変更'}],listeners:{click:function(a,b){switch(b.id){case 'delete':ModelController.deleteDiagram(selected_diagram_id);break;case 'open':open_diagram(g_model.diagrams[selected_diagram_id],selected_diagram_name,selected_diagram_id);break;case 'change':change_diagram_name_view(g_model.diagrams[selected_diagram_id]);break;}}}});l.on('itemmousedown',function(b,c,d,e,f){a.selected_diagram=g_model.diagrams[c.data.id];if(f.button==2){m.showAt(f.getX(),f.getY());selected_diagram_id=c.data.id;selected_diagram_name=c.data.text;}});Ext.getCmp('modelexplorer').removeAll();Ext.getCmp('modelexplorer').add(l);Ext.getCmp('modelexplorer').add({id:'element-infomation',xtype:'panel',width:200,height:200});this.panel=l;}ModelExplorer.prototype.open_diagram=function(a,b,c){return this.panel;};ModelExplorer.prototype.open_selected_diagram=function(){this.open_diagram(this.selected_diagram,this.selected_diagram.id);};ModelExplorer.prototype.open_diagram=function(a,b,c){var d=g_metamodel.metadiagrams[a.meta_id];var e;var f=c;if(f==undefined)if(d.instance_name!=null&&d.instance_name!=undefined){var g=g_metamodel.metaproperties[d.properties[d.instance_name]].id;var h=null;for(var i=0;i<a.properties.length;i++)if(a.properties[i].meta_id==g)h=a.properties[i];f=g_model.properties[h.children[0]].value;}if(d.seq==true)e=new SequenceEditor(f,b,a);else e=new DiagramEditor(f,b,a);editortabpanel.add(e,b);};function checkoutview(){$.post('/mvcs/group_rep_list',{},function(a){if(a){console.log('id\tname\thead_version');for(var b=0;b<a.length;b++)console.log(a[b].id+'\t'+a[b].name+'\t'+a[b].head_version);var c=Ext.create('Ext.selection.RowModel',{mode:'SINGLE',listeners:{selectionchange:function(a,b){for(var c=0;c<b.length;c++)console.log(c+'='+b[c].get('id'));}}});var d=Ext.create('Ext.window.Window',{title:'Checkout',height:200,width:400,layout:'fit',items:{xtype:'grid',border:false,columns:[{text:"name",dataIndex:'name'},{text:"head version",dataIndex:'head_version'}],store:Ext.create('Ext.data.Store',{data:a,fields:['id','name','head_version']}),selModel:c,dockedItems:[{xtype:'toolbar',dock:'bottom',ui:'footer',layout:{pack:'center'},items:[]},{xtype:'toolbar',items:[{text:'Checkout',tooltip:'checkout',iconCls:'add',handler:function(){console.log(''+c.getSelection()[0].get('id'));if(window.confirm('チェックアウトします。よろしいですか？'))checkout(c.getSelection()[0].get('id'),function(){d.hide();});}}]}]}}).show();}},"json");}function import_to_rep_view(){$.post('/mvcs/group_rep_list',{},function(a){if(a){console.log('id\tname\thead_version');for(var b=0;b<a.length;b++)console.log(a[b].id+'\t'+a[b].name+'\t'+a[b].head_version);var c=Ext.create('Ext.selection.RowModel',{mode:'SINGLE',listeners:{selectionchange:function(a,b){for(var c=0;c<b.length;c++)console.log(c+'='+b[c].get('id'));}}});var d=Ext.create('Ext.window.Window',{title:'Import',height:200,width:400,layout:'fit',items:{xtype:'grid',border:false,columns:[{text:"name",dataIndex:'name'},{text:"head version",dataIndex:'head_version'}],store:Ext.create('Ext.data.Store',{data:a,fields:['id','name','head_version']}),selModel:c,dockedItems:[{xtype:'toolbar',dock:'bottom',ui:'footer',layout:{pack:'center'},items:[]},{xtype:'toolbar',items:[{text:'Import',tooltip:'import',iconCls:'add',handler:function(){console.log(''+c.getSelection()[0].get('id'));if(window.confirm('リポジトリにインポートします。よろしいですか？'))import_to_rep(c.getSelection()[0].get('id'),function(){d.hide();});}}]}]}}).show();}},"json");}function delete_rep_view(){$.post('/mvcs/group_rep_list',{group_id:g_projectinfo.group.id},function(a){if(a){console.log('id\tname\thead_version');for(var b=0;b<a.length;b++)console.log(a[b].id+'\t'+a[b].name+'\t'+a[b].head_version);var c=Ext.create('Ext.selection.RowModel',{mode:'SINGLE',listeners:{selectionchange:function(a,b){for(var c=0;c<b.length;c++)console.log(c+'='+b[c].get('id'));}}});var d=Ext.create('Ext.window.Window',{title:'Delete',height:200,width:400,layout:'fit',items:{xtype:'grid',border:false,columns:[{text:"name",dataIndex:'name'},{text:"head version",dataIndex:'head_version'}],store:Ext.create('Ext.data.Store',{data:a,fields:['id','name','head_version']}),selModel:c,dockedItems:[{xtype:'toolbar',dock:'bottom',ui:'footer',layout:{pack:'center'},items:[]},{xtype:'toolbar',items:[{text:'Delete',tooltip:'delete',iconCls:'add',handler:function(){console.log(''+c.getSelection()[0].get('id'));if(window.confirm('リポジトリ「'+c.getSelection()[0].get('name')+'」を削除します。'))delete_rep(c.getSelection()[0].get('id'),function(){d.hide();});}}]}]}}).show();}},"json");}function update_to_ver_view(){$.post('/mvcs/ver_list',{pid:g_projectinfo.id},function(a){if(a){console.log('id\tversion\tcomment');for(var b=0;b<a.length;b++)console.log(a[b].id+'\t'+a[b].version+'\t'+a[b].content);var c=Ext.create('Ext.selection.RowModel',{mode:'SINGLE',listeners:{selectionchange:function(a,b){for(var c=0;c<b.length;c++)console.log(c+'='+b[c].get('version'));}}});var d=Ext.create('Ext.window.Window',{title:'update to previous version',height:200,width:400,layout:'fit',items:{xtype:'grid',border:false,columns:[{text:"version",dataIndex:'version'},{text:"comment",dataIndex:'content',width:160}],store:Ext.create('Ext.data.Store',{data:a,fields:['version','content']}),selModel:c,dockedItems:[{xtype:'toolbar',dock:'bottom',ui:'footer',layout:{pack:'center'},items:[]},{xtype:'toolbar',items:[{text:'update',tooltip:'update',iconCls:'add',handler:function(){console.log(''+c.getSelection()[0].get('version'));update_to_ver(c.getSelection()[0].get('version'),function(){d.hide();});}}]}]}}).show();}},"json");}function show_setting_diagram_name_window(a,b){Ext.Msg.prompt('ダイアグラム','ダイアグラム名を入力してください。',function(c,d){if(c!='cancel'){var e=ModelController.addDiagram(a);var f=g_metamodel.metadiagrams[e.meta_id];if(f.instance_name!=null&&f.instance_name!=undefined){var g=g_metamodel.metaproperties[f.properties[f.instance_name]].id;var h=null;for(var i=0;i<e.properties.length;i++)if(e.properties[i].meta_id==g)h=e.properties[i];g_model.properties[h.children[0]].value=d;}if(b!=null)b(e);g_modelExplorer=new ModelExplorer();win.hide();}},null,true,'');}function show_create_diagram_window(){var a=[];for(var b in g_metamodel.metadiagrams)a.push(g_metamodel.metadiagrams[b]);var c=Ext.create('Ext.selection.RowModel',{mode:'SINGLE',listeners:{selectionchange:function(a,b){for(var c=0;c<b.length;c++)console.log(c+'='+b[c].get('id'));}}});var d=Ext.create('Ext.window.Window',{title:'Diagram',height:200,width:400,layout:'fit',items:[{xtype:'grid',border:false,columns:[{text:"name",dataIndex:'name'}],store:Ext.create('Ext.data.Store',{data:a,fields:['id','name']}),selModel:c,dockedItems:[{xtype:'toolbar',dock:'bottom',ui:'footer',layout:{pack:'center'},items:[]},{xtype:'toolbar',items:[{text:'Create',tooltip:'create',iconCls:'add',handler:function(){show_setting_diagram_name_window(c.getSelection()[0].get('id'),null);}}]}]}]});d.show();}function change_diagram_name_view(a){Ext.Msg.prompt('ダイアグラム','名前の変更',function(b,c){if(b!='cancel'){var d=g_metamodel.metadiagrams[a.meta_id];if(d.instance_name!=null&&d.instance_name!=undefined){var e=g_metamodel.metaproperties[d.properties[d.instance_name]].id;var f=null;for(var g=0;g<a.properties.length;g++)if(a.properties[g].meta_id==e)f=a.properties[g];var h=new DiagramController(a);h.updateProperty(g_model.properties[f.children[0]],c,a);}g_modelExplorer=new ModelExplorer();}},null,false,'');}function HistoryView(a){Ext.create('Ext.data.Store',{storeId:'simpsonsStore',fields:['id','name'],data:{'items':a.verlist},proxy:{type:'memory',reader:{type:'json',root:'items'}}});var b=Ext.create('Ext.grid.Panel',{title:'Simpsons',store:Ext.data.StoreManager.lookup('simpsonsStore'),columns:[{header:'Id',dataIndex:'id'},{header:'Name',dataIndex:'name',flex:1}],height:200,width:400,selModel:new Ext.selection.RowModel({singleSelect:true,listeners:{select:{fn:function(a,b,c,d){Ext.Msg.alert('MetaObject',b.data.id+","+b.data);}}}})});var c=Ext.create('Ext.panel.Panel',{title:'MetaObjects',layout:{type:'hbox',align:'center'},items:[b,{xtype:'button',text:'add',handler:function(){alert('You clicked the button!');metaobjects.push(new MetaObject(metaobject_IdGenerator.getNewId(),''));}},{xtype:'button',text:'update',handler:function(){alert('You clicked the button!');}},{title:'Tool',layout:{type:'vbox',align:'center'},items:[{xtype:'button',text:'add',handler:function(){alert('You clicked the button!');}},{xtype:'button',text:'update',handler:function(){alert('You clicked the button!');}}]}],closable:'true'});}function ProjectInfoViewer(){var a='ID:'+g_project_id+'<br>NAME:'+g_projectinfo.name+'<br>REPOSITORY:'+g_projectinfo.rep_id;this.panel=Ext.create('Ext.panel.Panel',{title:'プロジェクト情報',html:a,closable:'true'});}ProjectInfoViewer.prototype.getPanel=function(){return this.panel;};ProjectInfoViewer.prototype.Initialize=function(){};ProjectInfoViewer.prototype.onActivate=function(){};function WelcomeMessageView(){var a=g_projectinfo.metamodel.welcome_message;this.panel=Ext.create('Ext.panel.Panel',{title:'ウェルカム',html:a,closable:'true'});}WelcomeMessageView.prototype.getPanel=function(){return this.panel;};WelcomeMessageView.prototype.Initialize=function(){};WelcomeMessageView.prototype.onActivate=function(){};