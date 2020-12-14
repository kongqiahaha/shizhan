var my_inf = new Vue({
  el: ".my_inf",
  data: {
    name: "",
    user_inf: {


    },
    is_loading:true,
    borrowed_arr: [],
  },
  methods: {
    return_book: function (book_id) {
      var that = this;
      axios
        .post("book_return", {
          book_id: book_id,
        })
        .then(function (request) {
          console.log(request);

          if (request.data.code === 200) {
            alert("归还失败，请稍后重试！");
          } else {

            location.href="/page4";
            alert("归还成功！");
          }
        })
        .catch(function (err) {
          console.log(err);
        });
    },

    get_borrow_value: function () {
      var that= this;
      axios.post("get_borrow_value").then(function (request) {
        console.log(request.data.code);
        if (request.data.code === 200) {
          alert("借书信息加载失败，请尝试刷新页面！");
        } else {
          that.borrowed_arr = request.data.borrowed_arr;
        }
      });
    },
    get_user_inf:function(){
      this.is_loading = true;
      var that= this;
      axios.get("get_user_inf").then(function (request) {
        console.log("request");
        that.user_inf = request.data.user_inf;
        console.log(request.data.user_inf);
        that.is_loading = false;
    }).catch(function (err) {
      console.log(err)
    })
  },
  },

  created: function () {
    this.get_user_inf();
    this.get_borrow_value();
  },
});
