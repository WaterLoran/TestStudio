import axios from "axios";

var instance = axios.create({
    headers: {
        'Content-Type': 'application/json'
    },
    timeout: 2500,
    // baseURL: "http://192.168.0.102:5000"
    baseURL: "http://192.168.0.106:5000"
})


export default instance
