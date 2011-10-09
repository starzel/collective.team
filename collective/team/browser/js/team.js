if(document.team === undefined){
    team = {};
}


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

