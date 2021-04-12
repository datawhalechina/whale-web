<template>
  <v-container fluid>
    <h2 v-text="article.title"></h2>
    <div v-html="article.content"></div>
  </v-container>
</template>

<script>
export default {
  name: 'ArticleDetail',
  data() {
    return {
      article: {
        title: '',
        content: '',
      },
    };
  },
  mounted() {
    const { id } = this.$route.params;
    this.$axios.get(`/articles/${id}`).then((data) => {
      this.article = { ...data.data };
    });
  },
};
</script>
