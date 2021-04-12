<template>
  <v-container fluid>
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
    <editor
      :api-key="api_key"
      :init="tiny"
      v-model="article.content"
      cloud-channel="5-stable"></editor>
    <v-btn
      :loading="loading"
      color="success"
      @click="save"
    >
      Save
      <v-icon right>mdi-content-save</v-icon>
    </v-btn>
  </v-container>
</template>

<script>
import Editor from '@tinymce/tinymce-vue';

export default {
  name: 'ArticleDetail',
  data() {
    return {
      loading: false,
      api_key: 'p71cr32cmowz59y5v09l0qt6zur14elj4yftbkhx432lggnp',
      id: null,
      article: {
        title: '',
        content: '',
      },
      tiny: {
        height: 500,
        menubar: false,
        // inline: true,
        plugins: [
          'advlist autolink lists link image charmap print preview anchor',
          'searchreplace visualblocks code fullscreen',
          'insertdatetime media table paste help wordcount codesample',
        ],
        toolbar: [
          'undo redo | formatselect | bold italic underline strikethrough backcolor | '
          + 'alignleft aligncenter alignright alignjustify | '
          + 'bullist numlist outdent indent | removeformat | help',
          'table tabledelete | image | codesample | code',
        ],
      },
    };
  },
  components: {
    Editor,
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
