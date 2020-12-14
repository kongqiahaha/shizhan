var app = new Vue({
  el: "#body",
  data() {
    return {
        info: {
        b_type: [],
        b_arr: [],
        b_keyword: "",
            is_loading:true
      }
    }

  },

  methods: {
    getValue: function () {
        this.info.is_loading =true;
      var that = this;
      axios.get("all_books").then(
        function (response) {
          console.log(response);
          that.info.b_arr = response.data.book_data;
          console.log(response.data.book_data);
          that.info.is_loading  = false;
        },
        function (err) {}
      );
    },

    select: function () {
        this.info.is_loading = true;
      var that = this;
      axios
        .get("search", {
          params: {
            // 通过作者或者书名查询
            keyword: that.info.b_keyword,
          },
        })
        .then(function (request) {
            that.info.is_loading = false;
            console.log(that.info.is_loading);
          console.log(request);
          if (request.code === 200) {
            alert("查询无果！");
          } else {
            that.info.b_arr = request.data.book_data_select;
          }
        })
        .catch(function (err) {
          console.log("error");
          console.log(that.b_keyword);
        });
    },
    borrow: function (b_id,is_borrowable) {
      var that = this;
      console.log(b_id);
      if(is_borrowable){
         axios
        .post("borrow", {
          book_id:b_id
        })
        .then(function (request) {
          console.log(request.data.code);
          if(request.data.code === 100){
            alert("借阅成功，请记得按时归还！")
             location.href="page2";
          }else{
              alert("借阅失败！")
            }

        })
        .catch(function (err) {
          console.log(err);
        });
      }

    },
  },
  created: function () {
    this.getValue();
  },
});
