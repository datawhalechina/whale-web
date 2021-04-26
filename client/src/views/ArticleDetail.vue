<template>
  <v-container fluid>
    <h2 v-text="article.title"></h2>
    <vue-markdown
      :source="article.content"
      :html="false"
    >
    </vue-markdown>
  </v-container>
</template>

<script>
import VueMarkdown from 'vue-markdown';

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
  components: {
    VueMarkdown,
  },
  mounted() {
    const { id } = this.$route.params;
    this.$axios.get(`/articles/${id}`).then((data) => {
      this.article = { ...data.data };
    });
  },
};
</script>
