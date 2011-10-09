if(document.team === undefined){
    team = {};
}
team.team_portlet_init = function(){
    require(["jquery-1.6.2", "dynatree"], function($){
        var elem = $("#dynatree_portlet");
        var tree = elem.dynatree({
            minExpandLevel:2,
            fx: { height: "toggle", duration: 100 },
            initAjax:{
                url:elem.attr('src')
            },
            onPostInit:function(node){
                var key = elem.attr("context");
                this.selectKey(key).activateSilently();
                this.getRoot().childList[1].setTitle("SIG-Startseite");
            },
            onActivate: function(node, event){
                window.location = node.data.href;
            }
        });
    });
};
team.add_wizard_init = function(){
    require(['underscore', 'jquery-1.6.2', 'jquery.tmpl', 'dynatree'], function(_, $){
        var tree = $("#dynatree").dynatree({
            minExpandLevel:2,
            initAjax:{
                url:"jsonview"
            },
            onActivate: function(node, event){
                if(node.data.isFolder){
                    if(_.any(node.childList, 
                             function(item) {return !item.data.isFolder;})){
                        return false;
                    }
                    node.addChild({'title': 'Bilder, PDFs oder Office Dokumente hinzufügen',
                                   'action': 'uploadify',
                                   'icon': false});
                    node.addChild({'title': 'Seite hinzufügen',
                                   'action': 'Document',
                                   'icon': false});
                    node.addChild({'title': 'Termin hinzufügen',
                                   'action': 'event',
                                   'icon': false});
                    node.addChild({'title': 'Ordner hinzufügen',
                                   'action': 'folder',
                                   'icon': false});
                    node.expand(true);
                }else{
                    var context = node.parent.data.key;
                    if(node.data.action == 'event'){
                        location.href = location.protocol + '//' 
                            + location.host + context + 
                            '/createObject?type_name=Event';
                    }else if (node.data.action == 'uploadify'){
                        location.href = location.protocol + '//' 
                            + location.host + context + 
                            '/@@upload';
                    }else if (node.data.action == 'Document'){
                        location.href = location.protocol + '//' 
                            + location.host + context + 
                            '/createObject?type_name=Document';
                    }else if (node.data.action == 'folder'){
                        $("#folderadd").show();
                        $("#path").val(context);
                    }
                }
                return false;
            }
        });

        $("#create_folder").click(function(){
            var spinner = $("#kss-spinner");
            var context = $("#context").val();
            var path = $("#path").val();
            var title = $("#title").val();
            spinner.show();
            $.get(context+'/addfolder', {path:path, title:title}, function(){
                $("#folderadd").hide();
                spinner.hide();
                var dtree = tree.dynatree('getTree');
                var active = dtree.getActiveNode().parent.data.key;
                dtree.options.onPostInit = function(){
                    tree.dynatree('getTree'). getNodeByKey(active).activateSilently();
                };
                dtree.reload();
            });
            return false;
        });
    });
};
team.send_document_init = function(){
    var users = [];
    var form = jq("#send_document");
    var warning = jq("#no_user_selected");
    require(['underscore', 'jquery-1.6.2'], function(_, $){
        var button = $("#send_document_button");
        var form = $("#send_document");
        button.click(function(){
            form.toggle();
        });
        form.find("input[name=submit]").click(function(e){
            warning.hide();
            var users = [];
            if (form.find("input[name=all]")[0].checked){
                users = _.reduce(form.find(".all_users"), function(reduced, item){
                    return reduced + ";" + item.value;
                }, "").slice(1);
            }else{
                users = _.reduce(form.find("#user-input-fields .list-field"), function(reduced, item){
                    return reduced + "," + item.value;
                }, "").slice(1);
            }
            if(users === ""){
                warning.show();
                return false;
            }
            var document_title = form.find("input[name=document_title]").val();
            var document_url = location.href;
            var user = form.find("input[name=current_user]").val();
            var body = "Hallo,%0A%0A" + user + ' möchte Sie auf das Dokument "' + 
                document_title + '" aus dem IDEA Intranet hinweisen:%0A%0A' + 
                document_url + '%0A%0AMit freundlichen Grüssen%0A%20%20%20%20Ihr IDEA Frankfurt Team';
            var href = "mailto:" + users + "?body=" + body;
                 
            href = href.replace(/ö/g, '%C3%B6')
                .replace(/ä/g, '%C3%A4')
                .replace(/ü/g, '%C3%BC')
                .replace(/ß/g, '%C3%9F')
                .replace(/ /g, '%20'); 
            location.href = href;
            return false;
    });

    });
    var autocomplete_context = form.find("#user-input-fields");
    var keys = jq.map(form.find(".all_users"), function(user){return [[jq(user).attr("value"), jq(user).attr("name")]];});
    autocomplete_context.data('klass','autocomplete-multiselection-widget list-field').data('title','None').data('input_type','checkbox');
    var input = autocomplete_context.find("#user").autocomplete(keys, {
        autoFill: true,
        minChars: 2,
        max: 10,
        mustMatch: true,
        matchContains: true,
        formatItem: function(row, idx, count, value) { 
            return row[1]; 
        },
        formatResult: function(row, idx, count) { 
            return ""; 
        }
    }).result(formwidget_autocomplete_ready);
    jq(".intranet_actions .ui-icon").tooltip();
};

team.startpage_init = function(){
    require(['jquery-1.6.2', 'jquery-ui-1.8.14'], function($){
        $(".pseudo_portlet_manager .noTeamMember").each(function(){
            var event_button = $(this).find('dt.portletHeader');
            var icons = $(this).find(".toggles");
            var contents = $(this).find('.portletItem');
            event_button.click(function(){
                icons.toggle();
                contents.toggle(50);
            });
        });
    });    
};

