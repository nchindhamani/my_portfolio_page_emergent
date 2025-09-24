import React, { useEffect } from 'react';
import { Card, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { Toaster } from './ui/toaster';
import { portfolioData } from '../data/portfolioData';
import { 
  Mail, 
  MapPin, 
  ExternalLink, 
  Calendar,
  Award,
  GraduationCap,
  Code,
  Database,
  Cloud,
  Terminal,
  CheckCircle
} from 'lucide-react';

const Portfolio = () => {
  // Smooth scroll effect
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('animate-fade-in');
          }
        });
      },
      { threshold: 0.1 }
    );

    const sections = document.querySelectorAll('.animate-on-scroll');
    sections.forEach((section) => observer.observe(section));

    return () => {
      sections.forEach((section) => observer.unobserve(section));
    };
  }, []);

  const scrollToSection = (sectionId) => {
    document.getElementById(sectionId)?.scrollIntoView({ 
      behavior: 'smooth',
      block: 'start'
    });
  };

  return (
    <div className="min-h-screen bg-white">
      {/* Navigation */}
      <nav className="fixed top-0 w-full bg-white/80 backdrop-blur-sm border-b border-gray-100 z-50">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex justify-between items-center">
            <div className="font-light text-lg tracking-tight">
              {portfolioData.personal.name}
            </div>
            <div className="hidden md:flex space-x-8">
              {['about', 'experience', 'skills', 'contact'].map((item) => (
                <button
                  key={item}
                  onClick={() => scrollToSection(item)}
                  className="text-sm font-normal tracking-wide hover:text-black transition-colors duration-300 capitalize"
                >
                  {item}
                </button>
              ))}
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="min-h-screen flex items-center justify-center px-6 pt-20">
        <div className="max-w-6xl mx-auto">
          <div className="grid md:grid-cols-2 gap-16 items-center">
            <div className="space-y-8">
              <div className="space-y-6">
                <h1 className="text-6xl md:text-7xl font-light tracking-tight leading-none">
                  {portfolioData.personal.name}
                </h1>
                <h2 className="text-2xl md:text-3xl font-light text-gray-600 tracking-wide">
                  {portfolioData.personal.title}
                </h2>
                <p className="text-lg font-light text-gray-500 leading-relaxed max-w-md">
                  {portfolioData.personal.tagline}
                </p>
              </div>
              
              <div className="flex items-center space-x-6 text-sm text-gray-600">
                <div className="flex items-center space-x-2">
                  <MapPin className="w-4 h-4" />
                  <span>{portfolioData.personal.location}</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Mail className="w-4 h-4" />
                  <span>{portfolioData.personal.email}</span>
                </div>
              </div>

              <Button 
                onClick={() => scrollToSection('contact')}
                className="px-8 py-3 bg-black text-white hover:bg-gray-800 transition-colors duration-300"
              >
                Get in touch
              </Button>
            </div>

            <div className="flex justify-center">
              <div className="relative">
                <div className="w-80 h-80 rounded-full overflow-hidden border-4 border-gray-100 shadow-lg">
                  <img 
                    src={portfolioData.personal.photo}
                    alt={portfolioData.personal.name}
                    className="w-full h-full object-cover"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="py-24 px-6 bg-gray-50">
        <div className="max-w-6xl mx-auto animate-on-scroll">
          <div className="grid md:grid-cols-2 gap-16">
            <div>
              <h3 className="text-4xl font-light tracking-tight mb-8">About</h3>
              <p className="text-lg font-light text-gray-700 leading-relaxed mb-6">
                {portfolioData.personal.summary}
              </p>
              <p className="text-lg font-light text-gray-700 leading-relaxed">
                After a focused career break for family caregiving, I'm actively upskilling and ready to bring my enhanced technical expertise back to the industry. My recent Python certification and continuous learning demonstrate my commitment to staying current with modern development practices.
              </p>
            </div>
            
            <div className="space-y-6">
              <div>
                <h4 className="text-lg font-normal mb-3">Current Focus</h4>
                <ul className="space-y-2 text-gray-600">
                  <li className="flex items-center space-x-2">
                    <CheckCircle className="w-4 h-4 text-green-600" />
                    <span>Python programming & modern frameworks</span>
                  </li>
                  <li className="flex items-center space-x-2">
                    <CheckCircle className="w-4 h-4 text-green-600" />
                    <span>Cloud technologies & AWS services</span>
                  </li>
                  <li className="flex items-center space-x-2">
                    <CheckCircle className="w-4 h-4 text-green-600" />
                    <span>Data analysis & visualization</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Experience Section */}
      <section id="experience" className="py-24 px-6">
        <div className="max-w-6xl mx-auto animate-on-scroll">
          <h3 className="text-4xl font-light tracking-tight mb-16 text-center">Experience</h3>
          
          <div className="space-y-12">
            {portfolioData.experience.map((exp, index) => (
              <Card key={index} className="border-0 shadow-sm">
                <CardHeader className="pb-4">
                  <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-4">
                    <CardTitle className="text-2xl font-light">{exp.company}</CardTitle>
                    <div className="text-sm text-gray-500 flex items-center space-x-2">
                      <Calendar className="w-4 h-4" />
                      <span>{exp.duration}</span>
                    </div>
                  </div>
                  <p className="text-lg text-gray-600 font-light">{exp.role}</p>
                </CardHeader>
                
                <CardContent>
                  <div className="space-y-8">
                    {exp.projects.map((project, pIndex) => (
                      <div key={pIndex} className="border-l-2 border-gray-100 pl-6">
                        <div className="mb-4">
                          <h4 className="text-lg font-normal">{project.client}</h4>
                          <p className="text-sm text-gray-600">{project.role} • {project.duration}</p>
                        </div>
                        
                        <ul className="space-y-2 mb-4">
                          {project.achievements.map((achievement, aIndex) => (
                            <li key={aIndex} className="text-gray-700 text-sm leading-relaxed">
                              • {achievement}
                            </li>
                          ))}
                        </ul>
                        
                        <div className="flex flex-wrap gap-2">
                          {project.techStack.map((tech, tIndex) => (
                            <Badge key={tIndex} variant="secondary" className="text-xs">
                              {tech}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Skills Section */}
      <section id="skills" className="py-24 px-6 bg-gray-50">
        <div className="max-w-6xl mx-auto animate-on-scroll">
          <h3 className="text-4xl font-light tracking-tight mb-16 text-center">Technical Skills</h3>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <Card className="border-0 shadow-sm">
              <CardHeader className="pb-4">
                <div className="flex items-center space-x-2 mb-2">
                  <Code className="w-5 h-5" />
                  <CardTitle className="text-lg font-normal">Languages</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {portfolioData.skills.languages.map((lang, index) => (
                    <Badge key={index} variant="outline" className="mr-2 mb-2">
                      {lang}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-sm">
              <CardHeader className="pb-4">
                <div className="flex items-center space-x-2 mb-2">
                  <Terminal className="w-5 h-5" />
                  <CardTitle className="text-lg font-normal">Frameworks</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {portfolioData.skills.frameworks.map((framework, index) => (
                    <Badge key={index} variant="outline" className="mr-2 mb-2">
                      {framework}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-sm">
              <CardHeader className="pb-4">
                <div className="flex items-center space-x-2 mb-2">
                  <Database className="w-5 h-5" />
                  <CardTitle className="text-lg font-normal">Databases</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {portfolioData.skills.databases.map((db, index) => (
                    <Badge key={index} variant="outline" className="mr-2 mb-2">
                      {db}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-sm">
              <CardHeader className="pb-4">
                <div className="flex items-center space-x-2 mb-2">
                  <Cloud className="w-5 h-5" />
                  <CardTitle className="text-lg font-normal">Cloud & Tools</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {[...portfolioData.skills.cloud, ...portfolioData.skills.tools.slice(0, 4)].map((tool, index) => (
                    <Badge key={index} variant="outline" className="mr-2 mb-2">
                      {tool}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Certifications */}
          <div className="mt-16">
            <h4 className="text-2xl font-light mb-8 text-center">Certifications & Education</h4>
            <div className="grid md:grid-cols-2 gap-8">
              <Card className="border-0 shadow-sm">
                <CardHeader>
                  <div className="flex items-center space-x-2 mb-2">
                    <Award className="w-5 h-5" />
                    <CardTitle className="text-lg font-normal">Certifications</CardTitle>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {portfolioData.certifications.map((cert, index) => (
                      <div key={index}>
                        <p className="font-medium">{cert.title}</p>
                        <p className="text-sm text-gray-600">{cert.issuer} • {cert.year}</p>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              <Card className="border-0 shadow-sm">
                <CardHeader>
                  <div className="flex items-center space-x-2 mb-2">
                    <GraduationCap className="w-5 h-5" />
                    <CardTitle className="text-lg font-normal">Education</CardTitle>
                  </div>
                </CardHeader>
                <CardContent>
                  <div>
                    <p className="font-medium">{portfolioData.education.degree}</p>
                    <p className="text-sm text-gray-600">{portfolioData.education.university}</p>
                    <p className="text-sm text-gray-600">{portfolioData.education.duration} • CGPA: {portfolioData.education.cgpa}</p>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="py-24 px-6">
        <div className="max-w-4xl mx-auto animate-on-scroll">
          <h3 className="text-4xl font-light tracking-tight mb-16 text-center">Get in Touch</h3>
          
          <div className="grid md:grid-cols-2 gap-16">
            <div>
              <h4 className="text-xl font-light mb-6">Let's connect</h4>
              <p className="text-gray-600 mb-8 leading-relaxed">
                I'm actively seeking new opportunities to contribute my technical expertise and fresh perspective. 
                Whether you're looking for a dedicated backend developer or someone with database optimization experience, 
                I'd love to discuss how I can add value to your team.
              </p>
              
              <div className="space-y-4">
                <div className="flex items-center space-x-3">
                  <Mail className="w-5 h-5 text-gray-500" />
                  <a href={`mailto:${portfolioData.personal.email}`} className="text-gray-700 hover:text-black transition-colors">
                    {portfolioData.personal.email}
                  </a>
                </div>
                <div className="flex items-center space-x-3">
                  <ExternalLink className="w-5 h-5 text-gray-500" />
                  <a 
                    href={portfolioData.personal.linkedin} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-gray-700 hover:text-black transition-colors"
                  >
                    LinkedIn Profile
                  </a>
                </div>
              </div>
            </div>

            <Card className="border-0 shadow-sm">
              <CardContent className="pt-6">
                <h4 className="text-xl font-light mb-6">Contact Information</h4>
                <div className="space-y-6">
                  <div>
                    <p className="text-gray-600 mb-4">
                      Feel free to reach out directly via email or connect with me on LinkedIn. I'm looking forward to discussing potential opportunities.
                    </p>
                  </div>
                  
                  <div className="space-y-4">
                    <div className="flex items-center space-x-3">
                      <MapPin className="w-5 h-5 text-gray-500" />
                      <span className="text-gray-700">{portfolioData.personal.location}</span>
                    </div>
                    
                    <div className="flex items-center space-x-3">
                      <Calendar className="w-5 h-5 text-gray-500" />
                      <span className="text-gray-700">Available for immediate start</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-6 bg-gray-50 border-t border-gray-100">
        <div className="max-w-6xl mx-auto text-center">
          <p className="text-sm text-gray-500">
            © 2025 {portfolioData.personal.name}. Ready to contribute to innovative projects.
          </p>
        </div>
      </footer>

      <Toaster />
    </div>
  );
};

export default Portfolio;