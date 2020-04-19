variable "do_token" {
    description = "DigitalOcean API Token"
}

variable "name" {
    description = "Name of the droplet to create"
}
variable "region" {
    description = "Datacenter region to create the droplet in"
}
variable "size" {
    description = "Specs for the droplet to create"
}

variable "image" {
  description = "OS Image to use for setting up droplet"
}

provider "digitalocean" {
  token = var.do_token
}

resource "digitalocean_droplet" "droplet" {
  image = var.image
  name   = var.name
  region = var.region
  size = var.size
}
