var notice = new Vue({
  el: ".allPage",
  data: {
    noticeArr: [],
    isShow: true,
    noticeArr2: [],
    showNotic: [true, false],
    isSuccess: false,
  },
  methods: {
    width: function () {
      console.log(innerWidth);
      if (innerWidth <= 980) {
        this.isShow = false;
      } else {
        this.isShow = true;
      }
    },
    test: function () {
      var that = this;
      axios.get("/static/json/index.json").then(
        function (response) {
          console.log(response.data.noticeArr);
          that.noticeArr = response.data.noticeArr;
          that.noticeArr2 = response.data.noticeArr2;
          console.log(that.isSuccess)
          that.isSuccess = true;
          console.log(that.isSuccess);
        },
        function (err) {}
      );
    },
    click: function () {
      console.log(this.noticeArr);
    },
  },
  mounted() {
    window.width = this.width;
    window.test = this.test;
  },
  created(){
    this.test();
  }
});
