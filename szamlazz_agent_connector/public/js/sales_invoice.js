frappe.ui.form.on('Sales Invoice',{
    setup(frm){
        let today = new Date()
        let tomorrow = new Date(today)
        tomorrow.setDate(tomorrow.getDate() + 1)
        frm.set_value('fullfilment_date', tomorrow)
    },

    on_submit(frm){
        window.open("/api/resource/salesinvoice/" + frm.name)
    }
    }
)
