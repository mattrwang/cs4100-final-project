import { Flex, Heading, Text, VStack } from "@chakra-ui/react";
import Navbar from "../Components/Navbar";

const Home = () => {
  return (
    <Flex flexDir="column">
      <Navbar />
      <Flex align="center" justify="center" pt="50px">
        <VStack
          bg="nugray.600"
          spacing={4}
          p={8}
          shadow="md"
          rounded="md"
          maxW="500px"
        >
          <Heading size="lg" textAlign="center">
            Welcome to the Northeastern Productivity App!
          </Heading>
          <Text textAlign="center">
            This is an app for Northeastern students, by Northeastern students.
            We aim to help you become more productive by helping you schedule
            your busy weeks and provide optimal times to study in Snell! Check
            out our pages to learn more!
          </Text>
          <Text pt="100px" textAlign="center" fontSize="12px" color="nugray.50">
            Created by Matthew Wang, Rup Jaisinghani, Julia Geller, Thomas
            Noochan
          </Text>
        </VStack>
      </Flex>
    </Flex>
  );
};

export default Home;
