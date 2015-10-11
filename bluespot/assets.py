from flask.ext.assets import Bundle

bundles = {


    'global_css': Bundle(
        'http://fonts.googleapis.com/css?family=Open+Sans:400,300,600,700&subset=all',
        'assets/global/plugins/font-awesome/css/font-awesome.min.css',
        'assets/global/plugins/simple-line-icons/simple-line-icons.min.css',
        'assets/global/plugins/bootstrap/css/bootstrap.min.css',
        'assets/global/plugins/uniform/css/uniform.default.css',
        'assets/global/css/components.css',
        'assets/global/css/plugins.css',
        'assets/global/plugins/datatables/plugins/bootstrap/dataTables.bootstrap.css', 
        'assets/global/plugins/bootstrap-toastr/toastr.min.css',
        output='gen/global.css'),
        
    'jquerry_js': Bundle(
        'assets/global/plugins/jquery.min.js',
        output='gen/jquerry.js'),

    'core_js': Bundle(
        'assets/global/plugins/jquery-ui/jquery-ui.min.js',
        'assets/global/plugins/bootstrap/js/bootstrap.min.js',
        'assets/global/plugins/bootstrap-hover-dropdown/bootstrap-hover-dropdown.min.js',
        'assets/global/plugins/jquery.blockui.min.js',
        'assets/global/plugins/uniform/jquery.uniform.min.js',
        'assets/global/plugins/bootstrap-toastr/toastr.min.js',
        output='gen/core.js'),

    'theme_css': Bundle(      
        'assets/admin/layout2/css/layout.css',
        'assets/admin/layout2/css/themes/grey.css',
        'assets/admin/layout2/css/custom.css',
        output='gen/admin_theme_css.css'),

    'theme_js': Bundle(      
        'assets/admin/pages/scripts/ui-blockui.js',

        output='gen/admin_theme_js.js'),

     'leads_js': Bundle(      
        'assets/admin/pages/scripts/ui-blockui.js',
        'assets/global/scripts/metronic.js',

        output='gen/admin_theme_js.js'),       

    #-------------------------Client specific assets-----------------------------------------------------
    'client_plugin_css': Bundle(
        output='gen/admin_plugin.css'),
        
    'client_page_css': Bundle(
        'assets/admin/pages/css/tasks.css',
        'assets/admin/pages/css/custom.css',
        #'assets/global/plugins/bootstrap-modal/css/bootstrap-modal-bs3patch.css',
        output='gen/admin_page_css.css'),           
    'client_landing_css': Bundle(
        #'assets/global/plugins/bootstrap-modal/css/bootstrap-modal-bs3patch.css',
        'assets/global/plugins/jquery-minicolors/jquery.minicolors.css',
        output='gen/client_landing_css.css'),  
                  
    'client_dashboard_script': Bundle(
        'assets/global/scripts/metronic.js',
        'assets/admin/layout2/scripts/layout.js',
        'assets/admin/layout2/scripts/demo.js',
        'assets/admin/pages/scripts/index.js',
        'assets/admin/pages/scripts/tasks.js',
        'assets/global/plugins/datatables/media/js/jquery.dataTables.min.js',
        'assets/global/plugins/datatables/plugins/bootstrap/dataTables.bootstrap.js',        
        output='gen/admin_dashboard_script.js'),      
        
    'client_dashboard_js': Bundle(
        'assets/custom/admin.js',
        'assets/global/scripts/metronic.js',
        output='gen/admin_dashboard.js'), 
        
	'client_manage_js': Bundle(
        'assets/global/scripts/metronic.js',
        'js/ajax-forms.js',
        'js/datatable.js',
        'assets/global/plugins/datatables/media/js/jquery.dataTables.min.js',
		'assets/global/plugins/datatables/plugins/bootstrap/dataTables.bootstrap.js',
		'assets/global/plugins/bootbox/bootbox.min.js',
        output='gen/client_manage.js'), 

    'client_landing_js': Bundle(
        'assets/global/scripts/metronic.js',
        'js/ajax-forms.js',
        'js/datatable.js',
        'js/files-upload.js',
        'assets/global/plugins/datatables/media/js/jquery.dataTables.min.js',
        'assets/global/plugins/datatables/plugins/bootstrap/dataTables.bootstrap.js',
        'assets/global/plugins/bootbox/bootbox.min.js',
        'assets/global/plugins/fancybox/source/jquery.fancybox.pack.js',
        'assets/global/plugins/plupload/js/plupload.full.min.js',
        'assets/global/plugins/jquery-minicolors/jquery.minicolors.min.js',
        output='gen/client_landing.js'), 
        
	'admin_feedback_js': Bundle(
		'assets/global/plugins/select2/select2.min.js',
        'assets/global/plugins/bootstrap-daterangepicker/moment.min.js',
        'assets/global/plugins/bootstrap-daterangepicker/daterangepicker.js',
		'assets/global/plugins/datatables/media/js/jquery.dataTables.min.js',
		'assets/global/plugins/datatables/plugins/bootstrap/dataTables.bootstrap.js',
		'assets/global/plugins/bootstrap-datepicker/js/bootstrap-datepicker.min.js',
        'assets/custom/feedback.js',
		output='gen/admin_feedback.js'),

    'admin_feedback_script': Bundle(
		'assets/global/scripts/metronic.js',
		'assets/admin/layout2/scripts/layout.js',
		'assets/admin/layout2/scripts/demo.js',
		'assets/global/scripts/datatable.js',
		'assets/admin/pages/scripts/table-managed.js',
        output='gen/admin_feedback_script.js'),

	'user_login_css':Bundle(
		'assets/admin/pages/css/login.css',
        output='gen/user_login_css.css')

}



