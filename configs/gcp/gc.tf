variable "region" {
    description = "Region to deploy the VM in"
}

variable "zone" {
  description = "Zone to deploy VM in"
}

variable "type" {
    description = "Type of machine to deploy"
}

variable "image" {
  description = "Image of OS to install"
}

provider "google" {
  credentials = file("creds.json")
  project     = "globespinner-xwpvfo"
  region      =  var.region
  zone        =  var.zone
}

resource "google_compute_instance" "vm_instance" {
  name = "globespinner-instance"
  machine_type = var.type

 boot_disk {
    initialize_params {
      image = var.image
    }  
  }

  network_interface {
    # A default network is created for all GCP projects
    network       = "default"
    access_config {
    }
  }
}