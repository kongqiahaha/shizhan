var classification = new Vue({
  el: ".classification",
  data() {
    return{
      info:{
         classification: [],
          book_arr: [],
          select: 1,
        is_loading:true,
      },
  }
  },
  methods: {
    getValue: function (index) {
      this.info.is_loading=true;
      console.log(this.info)
      var that = this;
      that.select = index;
      axios
        .post("get_class_value", {
          classification: index+1,
        })
        .then(function (response) {

          that.info.book_arr = response.data.books;


          console.log(that.info.is_loading)
        });
    },
    borrow: function (b_id,is_borrowable) {
      var that = this;
      if(is_borrowable){
        axios
        .post("borrow", {
          book_id: b_id,
        })
        .then(function (request) {
          console.log(request);
          if(request.data.code === 100){
            alert("借阅成功，请记得及时归还！");
             location.href="page1";
          }else{
            alert("借书失败！")
          }

        })
        .catch(function (err) {
          console.log(err);
        });
      }

    },
  },
  // 页面加载时执行
  created () {

    //请求获取分类信息
    var that = this;
    axios
      .get("classification")
      .then(function (request) {


        that.info.classification = request.data.b_type;

      })
      .catch(function (err) {
        console.log(err);
      });
      axios
        .get("all_books", {

        })
        .then(function (response) {

          that.info.book_arr = response.data.book_data;
          that.info.is_loading = false;
          console.log(that.info.is_loading)
        });
  },
});
