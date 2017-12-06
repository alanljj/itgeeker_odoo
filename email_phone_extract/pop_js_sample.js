https://stackoverflow.com/questions/44653154/odoo-8-how-to-create-a-button-that-contains-a-pop-up-message-with-a-refresh-of
To create the popup message you can assign a confirm attribute.

 <button name="toggle_active" type="object" confirm="(Un)archiving a forum automatically (un)archives its posts. Do you want to proceed?" class="oe_stat_button" icon="fa-archive">
This will prompt the user with a confirm dialog which you can use to convey your message and then after they click 'ok' it will execute your action.

<button name="test_dialog_then_action" type="object" class="oe_stat_button" icon="fa-check">
PYTHON Function

@api.multi
def test_dialog_then_action(self):
    return {
        'type':'ir.action.act_client',
        'tag': 'show_my_dialog'
    }
JS Script

odoo.define('addon_name.my_dialog', function(require){
"user strict";

var core = require('web.core');
var session = require('web.session');

var qweb = core.qweb;
var mixins = core.mixins;
var Widget = require('web.Widget');
var Model = require('web.Model');
var Dialog = require('web.Dialog');

function ActionShowDialog(parent, action){
    var dialog = new Dialog(document.body, {
        title: "Dialog Title",
        subtitle: "This is a subtitle!",
        size: 'medium',
        $content: "<div id='my_div'>Hello World!</div>",
        buttons: []
    });
    dialog.open();
    setTimeout(function(){
        dialog.close();
        new Model('your_addon.model_name')
        .call('func_name',arguments)
    }, 3000);
}

    core.action_registry.add("show_my_dialog", ActionShowDialog);
});
