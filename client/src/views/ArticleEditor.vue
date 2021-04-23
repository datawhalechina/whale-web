<template>
  <v-container fluid class="full-height">
    <v-row>
      <v-col
        cols="12"
        sm="12"
      >
        <v-text-field
          v-model="article.title"
          counter="64"
          label="Title"
        ></v-text-field>
      </v-col>
    </v-row>
    <v-row class="editor-container">
      <v-col
        cols="6"
        sm="6"
      >
        <textarea
          class="editor"
          label="Content (Markdown)"
          v-model="article.content"
          placeholder="Markdown"
        ></textarea>
      </v-col>
      <v-col
        cols="6"
        sm="6"
      >
        <vue-markdown
          class="result-html"
          :source="article.content"
          :html="false"
        >
        </vue-markdown>
      </v-col>
    </v-row>
    <v-row justify="end">
      <v-btn
        :loading="loading"
        color="success"
        @click="save"
      >
        Save
        <v-icon right>mdi-content-save</v-icon>
      </v-btn>
    </v-row>
  </v-container>
</template>

<style lang="scss" scoped>
.result-html {
  // vh, header, footer, title input, save button, container margin, row margin
  height: calc(100vh - 48px - 60px - 94px - 48px - 24px - 12px);
  padding: 2px 10px;
  overflow: scroll;
  background-color: #fff;
  border: 1px solid#ccc;
  border-radius: 4px;
  position: relative;
}
.editor-container {
  height: calc(100% - 94px - 36px);
  .editor {
    height: 100%;
    max-height: 100%;
    width: 100%;
    box-sizing: border-box;
    resize: none;
    outline: none;
    background-color: #f6f6f6;
    overflow-y: scroll;
    padding: 2px;
    border: 1px solid#ccc;
    border-radius: 4px;
  }
}
</style>

<script>
import VueMarkdown from 'vue-markdown';

export default {
  name: 'ArticleDetail',
  data() {
    return {
      loading: false,
      id: null,
      article: {
        title: '',
        content: '',
      },
    };
  },
  components: {
    VueMarkdown,
  },
  methods: {
    save() {
      this.loading = true;
      if (this.id !== null) {
        this.$axios.put(`/articles/${this.id}`, this.article).finally(() => {
          this.loading = false;
        });
      } else {
        this.$axios.post('/articles', this.article).finally(() => {
          this.loading = false;
        });
      }
    },
  },
  mounted() {
    const { id } = this.$route.params;
    if (id === 'add') {
      this.id = null;
    } else {
      this.id = id;
      this.$axios.get(`/articles/${id}`).then((data) => {
        const article = data.data;
        this.$set(this.article, {
          title: article.title,
          content: article.content,
        });
      });
    }
  },
};
</script>
