package user

import (
	"api_go_gateway/pkg/requestor"
	"github.com/gin-gonic/gin"
	"log"
)

type Handler struct {
	microserviceURL string
	path            string
	router          *gin.RouterGroup
	req             requestor.HTTPRequester
}

func NewHandler(router *gin.RouterGroup, microserviceURL string) *Handler {
	return &Handler{router: router, path: "auth", microserviceURL: microserviceURL}
}

func (s *Handler) Register() {
	AuthPath := s.router.Group(s.path)
	AuthPath.POST("/login", s.Login)
	AuthPath.POST("/registration", s.Registration)
	AuthPath.POST("/refresh_token", s.RefreshToken)
}

func (s *Handler) Login(c *gin.Context) {
	request := s.req.BuildRequest(
		"POST", s.microserviceURL+"/login", c.Request.URL.RawQuery, c.Request.Header, c.Request.Body,
	)
	r := s.req.Request(request)
	defer r.Body.Close()

	t, err := s.req.DecoderBody(r)
	if err != nil {
		log.Fatal(err)
	}

	c.JSON(r.StatusCode, t)
}

func (s *Handler) Registration(c *gin.Context) {
	request := s.req.BuildRequest(
		"POST", s.microserviceURL+"/registration", c.Request.URL.RawQuery, c.Request.Header, c.Request.Body,
	)
	r := s.req.Request(request)
	defer r.Body.Close()

	t, err := s.req.DecoderBody(r)
	if err != nil {
		log.Fatal(err)
	}

	c.JSON(r.StatusCode, t)
}

func (s *Handler) RefreshToken(c *gin.Context) {

	request := s.req.BuildRequest(
		"POST", s.microserviceURL+"/refresh_token", c.Request.URL.RawQuery, c.Request.Header, c.Request.Body,
	)
	r := s.req.Request(request)
	defer r.Body.Close()

	t, err := s.req.DecoderBody(r)
	if err != nil {
		log.Fatal(err)
	}

	c.JSON(r.StatusCode, t)
}
