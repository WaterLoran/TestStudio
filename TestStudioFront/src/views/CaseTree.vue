<template>
  <div>
    <form style="margin-top: 1rem">
      <v-row>
        <v-col cols="12" sm="6" md="4">
          <input type="file" @change="getFile($event)" />
          <v-divider vertical></v-divider>
          <input type="button" value="upload" @click="submit($event)">
        </v-col>
        <v-col cols="12" sm="6" md="4">
          <input type="button" value="使用选中的用例提交测试任务" @click="submit_test_task">
        </v-col>
      </v-row>
      <!-- 
      <input type="file" @change="getFile($event)" />
      <input type="button" value="upload" @click="submit($event)">
      <div>
        <input type="button" value="使用选中的用例提交测试任务" @click="submit_test_task">
      </div> -->

    </form>
    <v-divider></v-divider>
    <v-divider></v-divider>
    <v-treeview hoverable selectable selected-color="green" :items="items" v-model="selectedNodes"></v-treeview>
    <v-divider></v-divider>
  </div>
</template>

import axios from "axios";

<script>
import axios from 'axios'

export default {
  data: () => ({
    selectedNodes: [],
    items: [
      {
        id: 1,
        name: 'Applications :',
        children: [
          {
            id: 2,
            name: 'Calendar : app',
            children: [
              {
                id: 7,
                name: 'src :',
                children: [
                  { id: 8, name: 'index : ts' },
                ],
              },
            ],
          },
        ],
      },
      {
        id: 5,
        name: 'Documents :',
        children: [
          {
            id: 6,
            name: 'vuetify :',
            children: [
              {
                id: 7,
                name: 'src :',
                children: [
                  { id: 8, name: 'index : ts' },
                  { id: 9, name: 'bootstrap : ts' },
                ],
              },
            ],
          },
          {
            id: 10,
            name: 'material2 :',
            children: [
              {
                id: 11,
                name: 'src :',
                children: [
                  { id: 12, name: 'v-btn : ts' },
                  { id: 13, name: 'v-card : ts' },
                  { id: 14, name: 'v-window : ts' },
                ],
              },
            ],
          },
        ],
      },
    ],
    id_to_case_id: { 1: "case_0001" },
    exec_case_id_array: []
  }),
  created() {
    this.initialize()
  },

  methods: {

    initialize() {
      console.log("开始调用函数去获取数据")
      this.$api.testcase.getTestCase().then((result) => {
        console.log("getTestcase", result)
        this.items = result.data.items
        this.id_to_case_id = result.data.id_to_case_id
        console.log("id_to_case_id", this.id_to_case_id)
      }).catch((err) => {
        console.log(err)
      });
    },

    uploadcase() {
      this.$api.testcase.uploadcase().then((result) => {
        console.log("getTestcase", result)
        this.items = result.data.items
      }).catch((err) => {
        console.log(err)
      });
    },

    getFile: function (event) {
      this.file = event.target.files[0];
      console.log(this.file);
    },

    submit: function (event) {
      event.preventDefault();
      let formData = new FormData();
      formData.append("file", this.file);
      axios.post("http://192.168.0.106:5000/upload_case", formData).then(function (result) {
        console.log(result);
      }.bind(this)).catch(function (error) {
        alert("Fail");
        console.log(error);
      })

      // this.getSelectedNodeInfo();
    },

    submit_test_task() {
      // 获取选中的节点信息
      const selectedNodeIds = this.selectedNodes
      const id_to_case_id = this.id_to_case_id
      console.log("选中的节点信息：", selectedNodeIds)
      console.log("id_to_case_id", id_to_case_id)
      console.log("开始打印选中节点的信息");
      this.exec_case_id_array = []
      for (var value of selectedNodeIds) {
        // console.log(value);
        // console.log(id_to_case_id[value])
        this.exec_case_id_array.push(id_to_case_id[value])
      }
      console.log("结束打印选中节点的信息");
      console.log("this.exec_case_id_array", this.exec_case_id_array);

      this.$api.testtask.addTestTask(this.exec_case_id_array).then((result) => {
        console.log("addTestTask", result)
      }).catch((err) => {
        console.log("请求有误  ====>");
        console.log(err)
        console.log("请求有误  ====>");
      });
      console.log("提交测试任务结束");

    }



  }

}
</script>