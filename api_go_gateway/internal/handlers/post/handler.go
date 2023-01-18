package post

import (
	"api_go_gateway/internal/dto/posts"
	"api_go_gateway/internal/dto/user"
	"api_go_gateway/pkg/requestor"
	"fmt"
	"github.com/gin-gonic/gin"
	"log"
	"strconv"
)

type Handler struct {
	PostURLMicroservice string
	path                string
	router              *gin.RouterGroup
	client              requestor.HTTPRequester
	middlewares         []gin.HandlerFunc
}

func NewHandler(router *gin.RouterGroup, PostURLMicroservice string, middlewares []gin.HandlerFunc) *Handler {
	return &Handler{router: router, path: "/post", PostURLMicroservice: PostURLMicroservice, middlewares: middlewares}
}

func (s *Handler) Register() {
	PostPath := s.router.Group(s.path)
	s.SetMiddlewares(PostPath)

	PostPath.GET("", s.List)
	PostPath.GET("/:post_id", s.Get)
	PostPath.POST("/", s.Post)
	PostPath.PATCH("/:post_id", s.Patch)
	PostPath.DELETE("/:post_id", s.Delete)

	PostPath.GET("/:post_id/like", s.Like)
	PostPath.GET("/:post_id/dislike", s.Dislike)
}

func (s *Handler) SetMiddlewares(r *gin.RouterGroup) {
	for _, middleware := range s.middlewares {
		r.Use(middleware)
	}
}

func (s *Handler) List(c *gin.Context) {
	request := s.client.BuildRequest(
		"GET", s.PostURLMicroservice+"/", c.Request.URL.RawQuery, c.Request.Header, c.Request.Body,
	)
	r := s.client.Request(request)
	defer r.Body.Close()

	t, err := s.client.DecoderBody(r)
	if err != nil {
		log.Fatal(err)
	}

	c.JSON(r.StatusCode, t)

}

func (s *Handler) Get(c *gin.Context) {
	postID := c.Param("post_id")
	request := s.client.BuildRequest(
		"GET", fmt.Sprintf("%v/%v", s.PostURLMicroservice, postID), c.Request.URL.RawQuery, c.Request.Header, c.Request.Body,
	)
	r := s.client.Request(request)
	defer r.Body.Close()

	t, err := s.client.DecoderBody(r)
	if err != nil {
		log.Fatal(err)
	}

	c.JSON(r.StatusCode, t)
}

func (s *Handler) Post(c *gin.Context) {
	value, _ := c.Get("user")
	u := value.(user.User)

	var p posts.NewPost
	err := c.BindJSON(&p)
	if err != nil {
		log.Fatal(err)
	}
	p.BindUser(u)

	buffer, err := posts.ToBuffer(p)
	if err != nil {
		log.Fatal(err)
	}

	request := s.client.BuildRequest(
		"POST", s.PostURLMicroservice+"/", c.Request.URL.RawQuery, c.Request.Header, &buffer,
	)
	r := s.client.Request(request)
	defer r.Body.Close()

	t, err := s.client.DecoderBody(r)
	if err != nil {
		log.Fatal(err)
	}
	c.JSON(r.StatusCode, t)
}

func (s *Handler) Patch(c *gin.Context) {
	postID := c.Param("post_id")
	value, _ := c.Get("user")
	u := value.(user.User)

	var p posts.UpdatePost
	err := c.BindJSON(&p)
	if err != nil {
		log.Fatal(err)
	}
	p.BindUser(u)

	buffer, err := posts.ToBuffer(p)
	if err != nil {
		log.Fatal(err)
	}

	request := s.client.BuildRequest(
		"PATCH", fmt.Sprintf("%v/%v", s.PostURLMicroservice, postID),
		c.Request.URL.RawQuery, c.Request.Header, &buffer,
	)

	r := s.client.Request(request)
	defer r.Body.Close()

	t, err := s.client.DecoderBody(r)
	if err != nil {
		log.Fatal(err)
	}

	c.JSON(r.StatusCode, t)

}

func (s *Handler) Delete(c *gin.Context) {
	postID := c.Param("post_id")
	u, _ := c.Get("user")
	us := u.(user.User)

	q := c.Request.URL.Query()
	q.Set("user_id", strconv.Itoa(us.UserID))
	c.Request.URL.RawQuery = q.Encode()

	request := s.client.BuildRequest(
		"DELETE", fmt.Sprintf("%v/%v", s.PostURLMicroservice, postID),
		c.Request.URL.RawQuery, c.Request.Header, c.Request.Body,
	)

	r := s.client.Request(request)
	defer r.Body.Close()

	t, err := s.client.DecoderBody(r)
	if err != nil {
		c.JSON(r.StatusCode, make(map[string]string))
	}

	c.JSON(r.StatusCode, t)
}

func (s *Handler) Like(c *gin.Context) {

	c.JSON(200, []string{"heelo", "Like"})
}

func (s *Handler) Dislike(c *gin.Context) {

	c.JSON(200, []string{"heelo", "Dislike"})
}
