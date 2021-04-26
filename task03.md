## 熟悉首页需求并使用Vue实现首页功能

#### 前端代码目录结构
<img src="https://tva1.sinaimg.cn/large/008eGmZEly1gpqcaetmchj30p80qwtcb.jpg" width="350"/>

上图只列举了一些常用的文件，其他的文件如果小伙伴感兴趣，可参考文章 [vue项目文件结构](https://lq782655835.github.io/blogs/team-standard/recommend-vue-project-structure.html) 


#### Vue-Router简介

Vue-Router是Vue.js 官方的路由管理器，用简单的话说就是用来跳转页面并在页面跳转时可传递参数的一个工具，它包含的主要功能有：

- 嵌套的路由/视图表

- 模块化的、基于组件的路由配置

- 路由参数、查询、通配符

- 基于 Vue.js 过渡系统的视图过渡效果

##### 安装vue-router

- 通过NPM

    ```shell
    npm install vue-router
    ```
    
- 如果在一个模块化工程中使用它，必须要通过 Vue.use() 明确地安装路由功能：
    ```javascript
    import Vue from 'vue'
    import VueRouter from 'vue-router'
    Vue.use(VueRouter)
    ```
    
 - 如果使用全局的 script 标签，则无须如此 (手动安装)。

 - 其他的安装方式可参考[Vue-Router官网](https://router.vuejs.org/zh/installation.html)

    <hr/>

vue的路由是一个比较系统的知识点，需要花时间和精力去认真研究，对于新手来说，最常用到的就是路由页面跳转，下面列举几种路由跳转方式：

- ###### router-link（一般用于直接跳转，不通过方法调用的方式）
 ```javascript
    1. 不带参数
     
    <router-link :to="{name:'home'}"> 
    <router-link :to="{path:'/home'}"> 
    //name,path都行, 建议用name  
    // 注意：router-link中链接如果是'/'开始就是从根路由开始，如果开始不带'/'，则从当前路由开始。
     
    2.带参数
     
    <router-link :to="{name:'home', params: {id:1}}">  
     
    // params传参数 (类似post)
    // 在index.js中配置路由 path: "/home/:id" 或者 path: "/home:id" 
    // 不配置path ,第一次可请求,刷新页面id会消失
    // 配置path,刷新页面id会保留
     
    // html 取参  $route.params.id
    // script 取参  this.$route.params.id
     
    <router-link :to="{name:'home', query: {id:1}}"> 
     
    // query传参数 (类似get,url后面会显示参数)
    // 路由可不配置
     
    // html 取参  $route.query.id
    // script 取参  this.$route.query.id
 ```
- ##### this.$router.push() (函数里面调用)
 ```javascript
1.  不带参数
 
this.$router.push('/home')
this.$router.push({name:'home'})
this.$router.push({path:'/home'})
 
 
2. query传参 
 
this.$router.push({name:'home',query: {id:'1'}})
this.$router.push({path:'/home',query: {id:'1'}})
 
// html 取参  $route.query.id
// script 取参  this.$route.query.id
 
 
 
3. params传参
 
this.$router.push({name:'home',params: {id:'1'}})  // 只能用 name
 
// 路由配置 path: "/home/:id" 或者 path: "/home:id" ,
// 不配置path ,第一次可请求,刷新页面id会消失
// 配置path,刷新页面id会保留
 
// html 取参  $route.params.id
// script 取参  this.$route.params.id
 
 
 
4. query和params区别
query类似 get, 跳转之后页面 url后面会拼接参数,类似?id=1, 非重要性的可以这样传, 密码之类还是用params刷新页面id还在
 
params类似 post, 跳转之后页面 url后面不会拼接参数 , 但是刷新页面id 会消失
 ```

- ##### this.$router.replace() (用法同上,push)

- ##### this.$router.go(n) 

```javascript
this.$router.go(n) //向前或者向后跳转n个页面，n可为正整数或负整数

ps 区别:
this.router.push
跳转到指定url路径，并想history栈中添加一个记录，点击后退会返回到上一个页面

this.router.replace
跳转到指定url路径，但是history栈中不会有记录，点击返回会跳转到上上个页面 (就是直接替换了当前页面)

this.$router.go(n)
向前或者向后跳转n个页面，n可为正整数或负整数
```
关于VueRouter部分内容参考自[懂懂kkw的博客](https://blog.csdn.net/jiandan1127/article/details/86170336)，写的很清晰，分享给大家参考学习

**在初始项目中，路由存放在/router/index.js下，可参照学习**

#### vuex状态管理

Vuex 是一个专为 Vue.js 应用程序开发的**状态管理模式**。它采用集中式存储管理应用的所有组件的状态，并以相应的规则保证状态以一种可预测的方式发生变化。Vuex 也集成到 Vue 的官方调试工具 [devtools extension](https://github.com/vuejs/vue-devtools)，提供了诸如零配置的 time-travel 调试、状态快照导入导出等高级调试功能。用笔者的理解来说，就是给页面中的变量开辟了一个空间，用来存储记录它的的状态，以便在需要的时候可以全局调用

##### 通过npm安装vuex

```shell
npm install vuex --save
```

*其他的安装方式可参考[vuex官方文档](https://vuex.vuejs.org/zh/installation.html)*

##### 初步使用

```javascript
//安装完成后,在main.js中引入vuex
import store from './store'
//在实例中全局引用它
new Vue({
  store,
  render: (h) => h(App),
}).$mount('#app');

//在一般的store文件中，有几个概念，下面以初始项目中user.js中代码举例
export default {
  namespaced: true,  //命名空间，以免与其他store中的方法重名
  state: getInitialUserInfo(),  //记录状态的变量值
  getters, //想要在页面中获取store中的值，就得通过在getters里赋值，才能获取到
  actions, //在store中一般用来通过mutations改变state中变量的状态，
  mutations, //改变state中的变量状态
};
//如何使用的方法我以官网举的例子为大家解读一下
const store = new Vuex.Store({
  state: {
    count: 1
  },
  mutations: {   //在mutations中改变state中count的值,这只是一个方法
    increment (state) {
      // 变更状态
      state.count++
    }
  },
  actions:{
    increment ({commit}) {  //在这里执行，调用mutations中写好的方法，来改变，这时count的值就会增加
      commit('increment')
    }
  }
})

//如果大家想要在页面中改变store中的变量值
this.$store.dispatch('increment')   //在这里调用的是actions中的方法


以上就是vuex的基本使用啦，它还有很多的高级用法，期待小伙伴的学习和使用哦！
```

*vuex内容部分对于新手不太好理解，在本此实践中，大家只需要学会如何使用即可，等熟悉了一些再去了解原理*

**在初始项目中，store文件夹下存放的就是相关的内容**

#### 熟悉vuetify、material design组件库并使用

下面的内容就跟大家的实战息息相关啦，首先需要了解的就是前端框架vuetify的使用，material design是一个图标库，想让自己做出来的网页更加好看，当然图标是必不可少的。

##### vuetify的安装和使用

```shell
npm install vuetify
```

创建一个文件在 `src/plugins/vuetify.js` ，内容为：

```js
// src/plugins/vuetify.js

import Vue from 'vue'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'

Vue.use(Vuetify)

const opts = {}

export default new Vuetify(opts)
```

这样就可以开始使用啦

*对于刚接触前端的小伙伴来说，直接上来看文档可能会有点懵，内容太多，不知道应该怎么用，下面就为大家分析一下vuetify的文档结构*

<img src="https://tva1.sinaimg.cn/large/008i3skNly1gprd2xn9vfj30hq0k0dgs.jpg" width="350px"/>

上面的截图来自于[vuetify](https://vuetifyjs.com/en/getting-started/installation/#webpack-install)官网，红框中的内容是最常看的内容，**Styles and animations**里面是vuetify封装好的一些样式，可以直接使用，就不需要我们再另外写css！**UI Components**是我们常在页面中看到的一些元素组件，例如输入框，按钮等等；而**API**就是组件对应的属性和状态，例如按钮禁用，加载的状态就是靠API中的属性值来控制的。具体如何使用在文档中都有示例代码，大家可参考样例代码进行转换，变换为自己需要的。

##### material design的安装和使用

vuetify中集成了material design图标库，因此在使用的时候可以使用`<v-icon> 图标名 </v-icon>`就能看到图标了，图标库的链接[点这里查看](https://pictogrammers.github.io/@mdi/font/5.4.55/)，至于图标对应的属性，在vuetify中可查询到

------

以上知识点是在这次组队学习中可能涉及到或即将涉及到的，先给大家简略介绍一下，如果有遗漏的地方欢迎补充，下面带大家进入实操部分。说明：上面内容中讲解的代码均以组队学习初始代码为起点，提及的文件名也是项目中的，方便大家对照学习。

------

#### 基于交互图实现导航栏功能

前端部分实操的第一步：完成首页导航栏的基本跳转（**VueRouter**）与显示(**Vuetify的appBar或者ToolBars、List等组件**)

##### 1. 目标实现

<img src="https://tva1.sinaimg.cn/large/008i3skNly1gpxavql03fj327y06o0ue.jpg"/>

这是项目的初始运行效果

<img src="https://tva1.sinaimg.cn/large/008i3skNly1gpsigh2jbjj31rd079751.jpg" height="100px;" />

这是实现的简易版本的导航栏，给大家做个参考，大家基于初始代码更改，至于到底做成什么样式，大家可以自由发挥。不过需要实现基本的部分：

**导航栏需要有的栏目：首页，文章，领域，交流，榜单，是否登录注册状态显示，未登录状态下，点击图标，下拉列表项为登录；登录状态下，点击图标，出现下拉列表，项目为个人主页，人员管理，设置，注销登录**

1. 首页，文章，领域，交流，榜单需要跳转到相应的页面（**需要用到路由相关知识**），显示不同的内容，在本次组队学习中，侧重于实现领域模块和人员管理模块。
2. 需要前后端配合，实现登录注册功能
3. 领域模块：在编辑器中输入内容，点击发布，在领域页面可以看到发布的内容(**这里涉及到数据库的增删改查**)
4. 人员管理模块：人员角色分为管理员，用户，和游客，对于不同的身份，界面将呈现不同的内容，在组队学习中，具体体现在领域模块的管理，对于游客，只能够看过去发布的帖子；对于用户，可以发布帖子；对于管理员，可以管理用户发布的帖子，对其进行修改，删除等等操作。

可能涉及到的知识点：

- 前端：路由跳转，vuetify的使用，api请求，vuex状态管理，
- 后端：数据库的增删改查

**上面提到的是整个前端部分需要实现的模块，帮助大家更好的理解导航栏中的项目，大家先了解一下就好，后面会专门对这几个模块进行学习开发**

导航栏开发步骤(仅供参考)：

1. 运行初始项目
2. 了解代码结构，了解呈现的页面分别对应哪个文件，用了哪些组件
3. 找到导航栏所对应的文件，先把界面相关的部分实现，再与后端一起开发需要协作的部分

------

**PS：对于小白，上面内容可能不太好理解和应用，需要大家一点点慢慢开始，和大家一起讨论，学习，练习，就能改善。**

