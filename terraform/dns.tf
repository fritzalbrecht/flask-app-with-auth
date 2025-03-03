terraform {
  required_providers {
    cloudflare = {
      source = "cloudflare/cloudflare"
      version = "~> 4"
    }
  }
}

resource "cloudflare_record" "flaskapp_dns_record" {
  zone_id = var.cloudflare_zone_id
  name    = "flaskapp"
  value   = aws_lb.app_lb.dns_name
  type    = "CNAME"
  ttl     = 3600
  proxied = false
}