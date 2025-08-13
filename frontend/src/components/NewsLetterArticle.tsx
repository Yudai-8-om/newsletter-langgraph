import { Calendar } from "lucide-react";

const NewsletterArticle = () => (
  <div className="bg-white rounded-lg shadow-lg p-8 mb-12 max-w-4xl mx-auto">
    <div className="flex items-center justify-between mb-6">
      <h2 className="text-2xl font-bold text-gray-900">
        Daily Newsletter Sample
      </h2>
      <div className="flex items-center text-sm text-gray-500">
        <Calendar className="w-4 h-4 mr-1" />
        July 31st
      </div>
    </div>

    <div className="prose prose-gray max-w-none">
      <p className="text-gray-700 leading-relaxed mb-4">
        As the sun sets over the American West, a different kind of activity is
        taking center stage: the annual mating ritual of tarantulas. In states
        like California, Arizona, and Texas, male tarantulas are emerging from
        their burrows, their hairy bodies dusted with the golden hues of dusk.
        This fall, the arachnids are on the prowl, driven by a primal urge to
        find mates and ensure the survival of their species. While their
        presence might send shivers down the spine of an average homeowner,
        experts reassure that these ancient creatures pose no threat. 'They're
        more interested in avoiding predators than humans,' says Dr. Emily
        Carter, a zoologist at the University of Arizona. 'And they're harmless
        unless provoked.'
      </p>

      <p className="text-gray-700 leading-relaxed mb-4">
        Meanwhile, across the country, the economic landscape is also shifting.
        The Federal Reserve has decided to keep its benchmark interest rate
        unchanged at 4.25%-4.5%, a move that has sparked both relief and
        concern. Federal Reserve Chair Jerome Powell emphasized that the economy
        remains resilient despite rising inflation and the Trump
        administration's tariffs. 'The economy is in good shape, but we're
        navigating a delicate balance between inflation and growth,' Powell
        noted. The decision came amid dissent from two Fed governors, Michelle
        Bowman and Christopher Waller, who argued for a rate cut. Their rare
        disagreement highlights the growing divide over how to address economic
        challenges.
      </p>

      <p className="text-gray-700 leading-relaxed">
        For many Americans, these two stories reflect the dual realities of
        modern life: the quiet, cyclical rhythms of nature and the high-stakes
        game of economic policy. While tarantulas continue their dance of
        survival, the Fed's cautious approach signals a nation still grappling
        with the aftermath of inflation and global trade tensions. Whether the
        economy will shift toward growth or remain in a holding pattern depends
        on the same forces that drive the natural world—adaptation, resilience,
        and the unpredictable turn of events. As the leaves change and the
        markets shift, one thing is clear: the United States is in a state of
        constant motion, both above and below the surface.
      </p>
    </div>
  </div>
);

export default NewsletterArticle;
