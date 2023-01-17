frappe.ui.form.on('Sales Invoice',{
    customer(frm){
        let today = new Date()
        let tomorrow = new Date(today)
        tomorrow.setDate(tomorrow.getDate() + 1)
        frm.set_value('fulfillment_date', tomorrow)
    },

    on_submit(frm){
        window.open("/api/method/szamlazz_agent_connector.szamlazz_agent_connector.api.sales_invoice.download?doc_name=" + frm.doc.name)
    }
    }
)
