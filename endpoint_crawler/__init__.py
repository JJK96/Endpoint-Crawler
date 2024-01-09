def get_crawler(framework):
    match framework:
        case "spring_boot":
            from .frameworks.spring_boot import SpringBootCrawler
            return SpringBootCrawler()
        case _:
            raise Exception(f"Unsupported framework: {framework}")
            

def find_endpoints(dir, framework):
    crawler = get_crawler(framework)
    return crawler.find_endpoints(dir)
