package test

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping({"rest/endpoint"})
public class Controller {
   @PostMapping(
      value = {"request"},
      consumes = {"application/json"},
      produces = {"application/json"}
   )
   public Response request() {

   }

   @GetMapping(
      value = {"check"},
      produces = {"application/json"}
   )
   public Response check() {
    
   }
}
