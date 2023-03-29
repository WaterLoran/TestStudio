import axios from './http'

const testtask = {
    getTestTask(){
        return axios({
            method: "GET",
            url: "/test_task",
        })
    },
    addTestTask(in_data){
        console.log(in_data)
        return axios({
            method: "POST",
            url: "/test_task",
            // data: {"case_id_list": ['show_tags_001', 'show_tags_002', 'show_tables_001', 'show_tables_002']}
            data: {"case_id_list": in_data}
        })
    },
    updateTestTask(data){
        return axios({
            method: "PUT",
            url: "/test_task",
            data:data
        })
    },
    deleteTestTask(data){
        return axios({
            method: "DELETE",
            url: "/test_task",
            data: data
        })
    }
}

export default testtask