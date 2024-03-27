import React from "react";
import { Flex, Image, Spacer, Button } from "@chakra-ui/react";
import logo from "../Assets/Northeastern_Huskies_.svg";
import { Link as RouterLink } from "react-router-dom";

const Navbar = () => {
  return (
    <Flex
      as="nav"
      align="center"
      p="4"
      bg="nugray.700"
      width="full"
      maxH="75px"
      shadow="md"
    >
      <RouterLink to="/">
        <Image src={logo} alt="Logo" boxSize="75px" />
      </RouterLink>
      <Spacer />
      <Flex gap={4}>
        <Button
          colorScheme="nured"
          color="white"
          width="125px"
          as={RouterLink}
          to="/day"
        >
          Day Planning
        </Button>
        <Button
          colorScheme="nured"
          color="white"
          width="125px"
          as={RouterLink}
          to="/snell"
        >
          Snell Density
        </Button>
      </Flex>
    </Flex>
  );
};

export default Navbar;
