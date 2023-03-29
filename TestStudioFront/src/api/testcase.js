import axios from './http'

const testcase = {
    getTestCase(){
        return axios({
            method: "GET",
            url: "/test_case",
            // params: params
        })
    },
    addTestCase(data){
        return axios({
            method: "POST",
            url: "/testcase",
            data: data
        })
    },
    updateTestCase(data){
        return axios({
            method: "PUT",
            url: "/testcase",
            data:data
        })
    },
    deleteTestCase(data){
        return axios({
            method: "DELETE",
            url: "/testcase",
            data: data
        })
    },
    // uploadTestCase(e){
    //     const files = e.target.files
    //     const rawFile = files[0]
    //     let formData = new FormData()
    //     formData.append("files", rawFile)
        
    //     return axios({
    //       method: 'post',
    //       url: '/SZM/WuZiGuanLi/UpLoadWuZiImgExcel',
    //       data: formData,
    //       headers: {
    //         'Content-Type': 'multipart/form-data',
    //         'Authorization': localStorage.getItem("authorization")
    //       }
    //     })
    //   }
}

export default testcase