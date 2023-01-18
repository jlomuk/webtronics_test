package main

import (
	"api_go_gateway/internal/handlers/post"
	"api_go_gateway/internal/handlers/user"
	"api_go_gateway/internal/middlewares"
	"github.com/gin-gonic/gin"
	v3 "github.com/swaggest/swgui/v3cdn"
	"log"
)

const UserURLMicroservice = "http://localhost:8001/api/v1/auth"
const PostURLMicroservice = "http://localhost:8002/api/v1/post"

func SwaggerInit(r *gin.Engine) {
	swag := v3.NewHandler("swagger", "/docs/openapi.json", "/docs")
	r.GET("/docs", gin.WrapH(swag))
}

func main() {
	func() { log.SetFlags(log.Lshortfile | log.LstdFlags) }()
	r := gin.Default()
	r.Static("/docs", "./docs")

	SwaggerInit(r)

	api := r.Group("/api/v1/")

	UserHandlers := user.NewHandler(api, UserURLMicroservice)
	UserHandlers.Register()

	PostHandlers := post.NewHandler(api, PostURLMicroservice, []gin.HandlerFunc{middlewares.AuthMiddleware(UserURLMicroservice)})
	PostHandlers.Register()

	err := r.Run("0.0.0.0:9000")
	if err != nil {
		log.Fatal(err)
	}
}
