# Product Requirements Document (PRD)
## Captain Jack's UCF Bot: SHL Universal Competency Framework Learning Assistant

### 1. Executive Summary

**Product Name:** Captain Jack's UCF Bot (PUCF-Bot-v1)
**Version:** 1.0  
**Date:** December 2024  
**Owner:** Nabeel  

The PUCF-Bot-v1 is an interactive chatbot application designed to make learning about SHL's Universal Competency Framework (UCF) engaging and memorable through the charismatic persona of Captain Jack Sparrow from Pirates of the Caribbean. The bot combines educational content with entertainment to create an immersive learning experience.

### 2. Product Overview

#### 2.1 Problem Statement
- Traditional learning about competency frameworks can be dry and difficult to engage with
- Users need an interactive way to understand SHL's Universal Competency Framework
- Learning experiences should be memorable and enjoyable to improve retention

#### 2.2 Solution
A conversational AI chatbot that:
- Uses Captain Jack Sparrow's distinctive personality and speech patterns
- Explains SHL's UCF concepts through pirate-themed analogies
- Provides an interactive, engaging learning experience
- Makes complex competency concepts accessible and fun

### 3. Target Audience

#### 3.1 Primary Users
- HR professionals learning about competency frameworks
- Students studying organizational psychology or HR
- Consultants working with SHL assessments
- Anyone interested in understanding competency evaluation

#### 3.2 User Personas
- **HR Professional Helen**: Needs to understand UCF for employee evaluations
- **Student Sam**: Learning about competency frameworks in university
- **Consultant Chris**: Wants to explain UCF concepts to clients

### 4. Functional Requirements

#### 4.1 Core Features

**4.1.1 Chat Interface**
- Real-time conversational interface using Gradio
- Message-based interaction system
- Chat history preservation during session
- Example prompts to guide users

**4.1.2 AI Personality System**
- Captain Jack Sparrow persona implementation
- Distinctive speech patterns and pirate terminology
- Witty, charming, and slightly eccentric responses
- Consistent character maintenance

**4.1.3 Educational Content Delivery**
- SHL Universal Competency Framework expertise
- Competency assessment knowledge
- Performance and development insights
- Structured learning progression (Great 8 factors → competencies → components)

#### 4.2 Technical Features

**4.2.1 AI Integration**
- OpenAI GPT-4.1-nano model integration
- System prompt configuration for character consistency
- Message history management
- Response generation and delivery

**4.2.2 User Interface**
- Gradio ChatInterface implementation
- Web-based interface accessible via browser
- Example prompts for user guidance
- Clean, intuitive design

### 5. Non-Functional Requirements

#### 5.1 Performance
- Response time: < 3 seconds for typical queries
- Concurrent user support: Up to 10 simultaneous users
- Session persistence during active conversations

#### 5.2 Usability
- Intuitive chat interface requiring no training
- Clear example prompts to guide user interaction
- Responsive design for various screen sizes
- Accessible via standard web browsers

#### 5.3 Security
- Environment variable management for API keys
- No storage of personal user data
- Secure API communication with OpenAI

#### 5.4 Reliability
- Graceful error handling for API failures
- Consistent character personality maintenance
- Stable web interface operation

### 6. User Stories

#### 6.1 Learning UCF Concepts
**As a user**, I want to learn about SHL's Universal Competency Framework so that I can understand how to evaluate competencies effectively.

**Acceptance Criteria:**
- User can ask about UCF concepts and receive educational responses
- Responses are delivered in Captain Jack Sparrow's engaging style
- Information is accurate and follows the Great 8 factors structure

#### 6.2 Interactive Learning Experience
**As a user**, I want an engaging learning experience so that I can retain information better.

**Acceptance Criteria:**
- Responses use pirate-themed analogies and examples
- Learning is made fun and memorable
- Character personality is consistent throughout the conversation

#### 6.3 Guided Learning Path
**As a user**, I want structured guidance through UCF concepts so that I can learn systematically.

**Acceptance Criteria:**
- Bot starts with Great 8 factors when no specific direction is given
- Progressive learning from high-level concepts to detailed components
- Clear explanations of how competencies relate to performance

### 7. Technical Architecture

#### 7.1 Technology Stack
- **Backend:** Python
- **Frontend:** Gradio
- **AI Model:** OpenAI GPT-4.1-nano
- **Environment Management:** python-dotenv
- **Deployment:** Web-based application

#### 7.2 System Components
- **Chat Interface:** Gradio ChatInterface
- **AI Processing:** OpenAI API integration
- **Character System:** System prompt configuration
- **Environment Management:** .env file for API keys

#### 7.3 Data Flow
1. User inputs message through Gradio interface
2. Message passed to echo() function
3. OpenAI API called with system prompt and user message
4. AI response generated with Captain Jack Sparrow persona
5. Response returned to user through chat interface

### 8. User Experience Design

#### 8.1 Interface Design
- Clean, modern chat interface
- Example prompts prominently displayed
- Responsive design for various devices
- Intuitive message input and display

#### 8.2 Interaction Flow
1. User lands on chat interface
2. Example prompts guide initial interaction
3. User types question or selects example
4. Bot responds in Captain Jack Sparrow style
5. Conversation continues with educational content

#### 8.3 Example Prompts
- "I want to learn about the Universal Competency Framework (UCF)"
- "What is SHL?"
- "Why should I use SHL's UCF?"

### 9. Success Metrics

#### 9.1 Engagement Metrics
- Average session duration
- Number of messages per session
- User return rate
- Example prompt usage

#### 9.2 Educational Effectiveness
- User satisfaction with learning experience
- Accuracy of UCF information provided
- Character consistency maintenance
- Learning progression completion

### 10. Future Enhancements

#### 10.1 Short-term Improvements
- Additional example prompts
- Enhanced character responses
- Better error handling
- Mobile responsiveness improvements

#### 10.2 Long-term Vision
- Multi-language support
- Advanced competency assessment tools
- Integration with SHL's official resources
- Personalized learning paths
- Progress tracking and analytics

### 11. Risks and Mitigation

#### 11.1 Technical Risks
- **API Rate Limits:** Implement proper error handling and user feedback
- **Character Consistency:** Maintain robust system prompt configuration
- **Response Quality:** Regular testing and prompt optimization

#### 11.2 User Experience Risks
- **Over-characterization:** Balance entertainment with educational value
- **Information Accuracy:** Regular content review and updates
- **Accessibility:** Ensure interface works across different devices

### 12. Launch Plan

#### 12.1 MVP Features
- Basic chat interface with Captain Jack Sparrow persona
- Core UCF educational content
- Example prompts for user guidance
- Stable web deployment

#### 12.2 Launch Strategy
- Internal testing with HR professionals
- Beta testing with target user groups
- Gradual rollout with feedback collection
- Documentation and user guides

### 13. Appendices

#### 13.1 Technical Dependencies
- OpenAI API access and credentials
- Python environment setup
- Gradio library installation
- Environment variable configuration

#### 13.2 Character Guidelines
- Maintain Captain Jack Sparrow's distinctive speech patterns
- Use pirate terminology and sea-related metaphors
- Balance entertainment with educational content
- Keep responses concise but engaging (2-4 paragraphs)

---

**Document Version:** 1.0  
**Last Updated:** December 2024  
**Next Review:** January 2025
